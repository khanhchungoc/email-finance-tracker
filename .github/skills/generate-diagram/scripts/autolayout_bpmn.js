import fs from 'node:fs';

/**
 * Enhanced BPMN 2.0 Auto-Layout & Post-Processing Utility
 * Enforces 6 Core Layout Rules from bpmn-guide.md:
 * 1. Same-Lane Progression: Keep going horizontally right along main center spine.
 * 2. Lane-Change Continuation: Direct 0-turn vertical alignment if clear; Right-Up / Right-Down staggering if overlapping arrows/nodes.
 * 3. Minimal Competing Anchors: Clean port distribution (Left=in, Right=out, Top/Bottom=rejection/loop) to prevent arrowhead collisions.
 * 4. Horizontal Row Alignment & Secondary Rows: Nodes on the same line are aligned on Center-Y; create secondary parallel rows in the swimlane if overlapping.
 * 5. Leftward / Loopback Flow Routing: Choose the port with fewest turns and least overlap; never force Right-exit for leftward flows.
 * 6. Node Nudge-to-Align: If nudging a node by ≤35px makes a connecting flow straight (0 turns), move the node and collapse the edge to 2 waypoints (no sibling overlap check first).
 * - Dynamic Node-Based Spacing: Canvas scales dynamically based on column count (no hardcoded limits).
 * - Enforces Exclusive Gateway default attributes & 15px label offsets.
 */
async function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Usage: node autolayout_bpmn.js <path-to-bpmn-file>');
    process.exit(1);
  }

  let layoutProcess;
  try {
    const mod = await import('bpmn-auto-layout');
    layoutProcess = mod.layoutProcess;
  } catch (importErr) {
    console.error(`Failed to load bpmn-auto-layout package: ${importErr.message}`);
    process.exit(1);
  }

  try {
    const xml = fs.readFileSync(filePath, 'utf-8');
    let layoutedXml = xml;

    // If XML does not yet contain visual Participant/Lane DI shapes, run auto-layout engine
    if (!xml.includes('bpmndi:BPMNShape id="Lane_') && !xml.includes('bpmndi:BPMNShape id="Participant_')) {
      const result = await layoutProcess(xml);
      layoutedXml = typeof result === 'string' ? result : (result.xml || result);
      if (!layoutedXml || typeof layoutedXml !== 'string') {
        throw new Error('layoutProcess returned empty or invalid XML result');
      }
    } else {
      console.log('[Lane Preservation] Preserving pre-existing visual Swimlane & Pool DI layout bounds.');
    }

    // Run Automated Guide Checks & Enhancements (Multilane Alignment, Competing Anchors, Default Attributes, Label Offsets)
    const enhancedXml = postProcessBpmn(layoutedXml);

    fs.writeFileSync(filePath, enhancedXml, 'utf-8');
    console.log(`Successfully auto-formatted & validated multi-lane BPMN layout: ${filePath}`);
  } catch (err) {
    console.error(`BPMN Auto-layout error: ${err.message}`);
    process.exit(1);
  }
}

/**
 * Applies automated post-processing rules from bpmn-guide.md
 */
function postProcessBpmn(xml) {
  let processed = xml;

  // Rule 0: Compress excessive horizontal spacing from default auto-layout grid
  processed = compressHorizontalSpacing(processed);

  // Gateway Branch Stacking: Align nodes vertically if branched from same gateway in same lane
  processed = stackSameLaneGatewayBranches(processed);

  // Rule 1: Vertical Swimlane & Pool Shrink-Wrapping
  processed = shrinkWrapSwimlanesAndPools(processed);

  // Rule 2: Dock Boundary Events onto host activity shape perimeters
  processed = dockBoundaryEvents(processed);

  // Rule 3: Apply BPMN-in-Color standard visual palette
  processed = applyBpmnInColor(processed);

  // Rule 4: Ensure Exclusive Gateways with multiple outgoing flows declare a default attribute
  processed = processed.replace(/<bpmn:exclusiveGateway\s+([^>]+)>/g, (match, attrs) => {
    if (!attrs.includes('default=')) {
      const idMatch = attrs.match(/id="([^"]+)"/);
      if (idMatch) {
        const gwId = idMatch[1];
        const outgoingRegex = new RegExp(`<bpmn:sequenceFlow[^>]+sourceRef="${gwId}"[^>]+id="([^"]+)"`, 'g');
        const firstOutgoing = outgoingRegex.exec(xml);
        if (firstOutgoing) {
          console.log(`[Auto-Fix] Added missing default attribute on Exclusive Gateway '${gwId}' -> default='${firstOutgoing[1]}'`);
          return `<bpmn:exclusiveGateway ${attrs} default="${firstOutgoing[1]}">`;
        }
      }
    }
    return match;
  });

  // Rule 5: Ensure Sequence Flow labels sit at least 15px above horizontal edge waypoints
  processed = processed.replace(/<bpmndi:BPMNEdge\s+([^>]+)>([\s\S]*?)<\/bpmndi:BPMNEdge>/g, (match, edgeAttrs, content) => {
    const waypoints = [];
    const wpRegex = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
    let wpMatch;
    while ((wpMatch = wpRegex.exec(content)) !== null) {
      waypoints.push({ x: parseFloat(wpMatch[1]), y: parseFloat(wpMatch[2]) });
    }

    if (waypoints.length >= 2 && content.includes('<bpmndi:BPMNLabel>')) {
      const labelMatch = content.match(/<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/);
      if (labelMatch) {
        const lx = parseFloat(labelMatch[1]);
        let ly = parseFloat(labelMatch[2]);
        const lw = parseFloat(labelMatch[3]);
        const lh = parseFloat(labelMatch[4]);

        for (let i = 0; i < waypoints.length - 1; i++) {
          const p1 = waypoints[i];
          const p2 = waypoints[i + 1];
          if (Math.abs(p1.y - p2.y) < 2) {
            const segY = p1.y;
            const minX = Math.min(p1.x, p2.x);
            const maxX = Math.max(p1.x, p2.x);

            if (lx + lw >= minX && lx <= maxX && ly <= segY && ly + lh >= segY - 5) {
              const targetY = segY - lh - 15;
              content = content.replace(
                `y="${labelMatch[2]}"`,
                `y="${targetY.toFixed(0)}"`
              );
              break;
            }
          }
        }
      }
    }

    return `<bpmndi:BPMNEdge ${edgeAttrs}>${content}</bpmndi:BPMNEdge>`;
  });

  // Rule 6: Active Auto-Repair of Competing Anchor Port Distribution
  processed = repairAnchorPortDistribution(processed);

  // Rule 7: Active Rerouting of Leftward / Loopback Flows
  processed = rerouteLeftwardFlows(processed);

  // Rule 8: Nudge nodes to align with connecting flows (reduces turns to 0 where possible)
  processed = nudgeNodesToStraightenFlows(processed);

  // Rule 9: Enforce 100% Orthogonal Edge Routing & Shape Perimeter Touch
  processed = enforceOrthogonalAndTouchingWaypoints(processed);

  // Rule 10: Strip invalid semantic attributes from DI elements
  processed = stripInvalidDiAttributes(processed);

  // Final Audits & Sanity Inspectors
  auditLineShapeCollisions(processed);
  auditAnchorPortDistribution(processed);
  auditLeftwardFlowRouting(processed);

  return processed;
}

/**
 * Audits all sequence flow edge segments against shape bounds to detect arrow-node collisions
 */
function auditLineShapeCollisions(xml) {
  const shapes = [];
  const shapeRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>[\s\S]*?<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/g;
  let sMatch;
  while ((sMatch = shapeRegex.exec(xml)) !== null) {
    const sId = sMatch[1].toLowerCase();
    const eId = sMatch[2].toLowerCase();
    if (sId.includes('participant') || sId.includes('lane') || eId.includes('participant') || eId.includes('lane')) continue;
    shapes.push({
      shapeId: sMatch[1],
      elementId: sMatch[2],
      x: parseFloat(sMatch[3]),
      y: parseFloat(sMatch[4]),
      w: parseFloat(sMatch[5]),
      h: parseFloat(sMatch[6])
    });
  }

  const edgeRegex = /<bpmndi:BPMNEdge\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>([\s\S]*?)<\/bpmndi:BPMNEdge>/g;
  const flowSourceTargetMap = {};
  const flowRegex = /<bpmn:sequenceFlow\s+([^>]+)>/g;
  let fMatch;
  while ((fMatch = flowRegex.exec(xml)) !== null) {
    const attrs = fMatch[1];
    const idM = attrs.match(/id="([^"]+)"/);
    const srcM = attrs.match(/sourceRef="([^"]+)"/);
    const tgtM = attrs.match(/targetRef="([^"]+)"/);
    if (idM && srcM && tgtM) {
      flowSourceTargetMap[idM[1]] = { sourceRef: srcM[1], targetRef: tgtM[1] };
    }
  }

  let eMatch;
  let collisionCount = 0;
  while ((eMatch = edgeRegex.exec(xml)) !== null) {
    const flowId = eMatch[2];
    const mapping = flowSourceTargetMap[flowId] || {};
    const waypoints = [];
    const wpRegex = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
    let wpMatch;
    while ((wpMatch = wpRegex.exec(eMatch[3])) !== null) {
      waypoints.push({ x: parseFloat(wpMatch[1]), y: parseFloat(wpMatch[2]) });
    }

    for (let i = 0; i < waypoints.length - 1; i++) {
      const p1 = waypoints[i];
      const p2 = waypoints[i + 1];

      for (const shape of shapes) {
        if (shape.elementId === mapping.sourceRef || shape.elementId === mapping.targetRef) continue;

        if (lineIntersectsRect(p1.x, p1.y, p2.x, p2.y, shape.x + 2, shape.y + 2, shape.w - 4, shape.h - 4)) {
          collisionCount++;
          console.warn(`[Collision Warning] Flow '${flowId}' segment (${p1.x},${p1.y})->(${p2.x},${p2.y}) intersects shape '${shape.elementId}'`);
        }
      }
    }
  }

  if (collisionCount === 0) {
    console.log('[Collision Audit] Clean! 0 arrow-node line collisions detected.');
  }
}

/**
 * Audits anchor port distribution on all shapes to ensure no two flows compete for the exact same pixel anchor
 */
function auditAnchorPortDistribution(xml) {
  const nodeFlows = new Map();
  const flowMap = new Map();
  const fRegex = /<bpmn:sequenceFlow\s+([^>]+)>/g;
  let fm;
  while ((fm = fRegex.exec(xml)) !== null) {
    const attrs = fm[1];
    const idM = attrs.match(/id="([^"]+)"/);
    const srcM = attrs.match(/sourceRef="([^"]+)"/);
    const tgtM = attrs.match(/targetRef="([^"]+)"/);
    if (idM && srcM && tgtM) {
      flowMap.set(idM[1], { src: srcM[1], tgt: tgtM[1] });
      nodeFlows.set(srcM[1], (nodeFlows.get(srcM[1]) || 0) + 1);
      nodeFlows.set(tgtM[1], (nodeFlows.get(tgtM[1]) || 0) + 1);
    }
  }

  const portUsage = {};
  const edgeRegex = /<bpmndi:BPMNEdge\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>([\s\S]*?)<\/bpmndi:BPMNEdge>/g;
  let eMatch;

  while ((eMatch = edgeRegex.exec(xml)) !== null) {
    const flowId = eMatch[2];
    const waypoints = [];
    const wpRegex = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
    let wpMatch;
    while ((wpMatch = wpRegex.exec(eMatch[3])) !== null) {
      waypoints.push({ x: parseFloat(wpMatch[1]), y: parseFloat(wpMatch[2]) });
    }

    if (waypoints.length >= 2) {
      const startWp = `${waypoints[0].x},${waypoints[0].y}`;
      const endWp = `${waypoints[waypoints.length - 1].x},${waypoints[waypoints.length - 1].y}`;
      
      const flow = flowMap.get(flowId);
      if (flow) {
        portUsage[startWp] = portUsage[startWp] || [];
        portUsage[startWp].push({ flowId, role: 'exit', node: flow.src });

        portUsage[endWp] = portUsage[endWp] || [];
        portUsage[endWp].push({ flowId, role: 'entry', node: flow.tgt });
      }
    }
  }

  let duplicateCount = 0;
  for (const [wpKey, flows] of Object.entries(portUsage)) {
    if (flows.length > 1) {
      const firstNode = flows[0].node;
      const allSameNode = flows.every(f => f.node === firstNode);
      const allSameRole = flows.every(f => f.role === flows[0].role);
      
      // High-Density Node Exception: allow overlap if node has > 4 flows and all overlapping flows share the same direction
      if (allSameNode && allSameRole && nodeFlows.get(firstNode) > 4) {
        continue;
      }

      duplicateCount++;
      const flowIds = flows.map(f => `${f.flowId} (${f.role})`).join(', ');
      console.warn(`[Anchor Port Warning] Competing anchor port detected at waypoint (${wpKey}) shared by: ${flowIds}`);
    }
  }

  if (duplicateCount === 0) {
    console.log('[Anchor Port Audit] Clean! 0 competing anchor port collisions detected.');
  }
}

/**
 * Checks if line segment (x1,y1)->(x2,y2) intersects rectangle (rx, ry, rw, rh)
 */
function lineIntersectsRect(x1, y1, x2, y2, rx, ry, rw, rh) {
  const minX = Math.min(x1, x2);
  const maxX = Math.max(x1, x2);
  const minY = Math.min(y1, y2);
  const maxY = Math.max(y1, y2);

  if (maxX <= rx || minX >= rx + rw || maxY <= ry || minY >= ry + rh) return false;

  if (Math.abs(y1 - y2) < 1) {
    return y1 > ry && y1 < ry + rh && maxX > rx && minX < rx + rw;
  }
  if (Math.abs(x1 - x2) < 1) {
    return x1 > rx && x1 < rx + rw && maxY > ry && minY < ry + rh;
  }

  return true;
}

/**
 * Automatically compresses wide horizontal spacing produced by default auto-layout grid engines
 */
function compressHorizontalSpacing(xml) {
  const pMatch = xml.match(/<bpmndi:BPMNShape\s+id="BPMNShape_Participant_[^"]+"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/);
  if (!pMatch) return xml;

  const origWidth = parseFloat(pMatch[4]);
  const minX = parseFloat(pMatch[2]) || 60;

  // Dynamically detect unique node column X-positions
  const uniqueCols = new Set();
  const colRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"/g;
  let cMatch;
  while ((cMatch = colRegex.exec(xml)) !== null) {
    if (!cMatch[1].includes('Participant') && !cMatch[1].includes('Lane')) {
      uniqueCols.add(Math.round(parseFloat(cMatch[2]) / 20) * 20);
    }
  }
  const colCount = uniqueCols.size || 10;

  // Calculate dynamic target canvas width based on actual column count (110px node width + 45px gap + margins)
  const targetWidth = Math.round(minX + (colCount * 110) + Math.max(0, colCount - 1) * 45 + 120);

  if (origWidth <= targetWidth) return xml; // Already dynamic & compact

  const scaleX = (targetWidth - minX) / (origWidth - minX);
  console.log(`[Dynamic-Spacing] Scaled horizontal layout dynamically based on ${colCount} node columns (Scale Factor: ${scaleX.toFixed(2)}, Canvas Width: ${origWidth}px -> ${targetWidth}px)`);

  const oldShapes = {};
  const newShapes = {};
  const sRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/g;
  let m;
  while ((m = sRegex.exec(xml)) !== null) {
    const shapeId = m[1];
    const elemId = m[2];
    const x = parseFloat(m[3]);
    const y = parseFloat(m[4]);
    const w = parseFloat(m[5]);
    const h = parseFloat(m[6]);
    oldShapes[elemId] = { x, y, w, h };
    const newX = Math.round(minX + (x - minX) * scaleX);
    newShapes[elemId] = { x: newX, y, w: (shapeId.includes('Participant') || shapeId.includes('Lane')) ? Math.round(w * scaleX) : w, h };
  }

  let res = xml;

  res = res.replace(/(<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x=")([^"]+)("\s+y="[^"]+"\s+width=")([^"]+)(")/g, (match, p1, shapeId, elemId, xVal, p2, wVal, p3) => {
    const ns = newShapes[elemId];
    if (ns) {
      return `${p1}${ns.x}${p2}${ns.w}${p3}`;
    }
    return match;
  });

  res = res.replace(/(<bpmndi:BPMNEdge\s+id="[^"]+"\s+bpmnElement="([^"]+)"[^>]*>)([\s\S]*?)(<\/bpmndi:BPMNEdge>)/g, (match, eStart, flowId, eContent, eEnd) => {
    const fRegex = new RegExp(`<bpmn:sequenceFlow\\s+id="${flowId}"\\s+sourceRef="([^"]+)"\\s+targetRef="([^"]+)"`);
    const fMatch = xml.match(fRegex);
    const sourceRef = fMatch ? fMatch[1] : null;
    const targetRef = fMatch ? fMatch[2] : null;

    const sOld = oldShapes[sourceRef];
    const sNew = newShapes[sourceRef];
    const tOld = oldShapes[targetRef];
    const tNew = newShapes[targetRef];

    let newContent = eContent.replace(/<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"\s*\/>/g, (wMatch, xVal, yVal) => {
      const wx = parseFloat(xVal);
      const wy = parseFloat(yVal);

      if (sOld && sNew && Math.abs(wx - (sOld.x + sOld.w)) < 5) {
        return `<di:waypoint x="${sNew.x + sNew.w}" y="${wy}" />`;
      }
      if (sOld && sNew && Math.abs(wx - sOld.x) < 5) {
        return `<di:waypoint x="${sNew.x}" y="${wy}" />`;
      }
      if (sOld && sNew && Math.abs(wx - (sOld.x + sOld.w / 2)) < 5) {
        return `<di:waypoint x="${Math.round(sNew.x + sNew.w / 2)}" y="${wy}" />`;
      }

      if (tOld && tNew && Math.abs(wx - tOld.x) < 5) {
        return `<di:waypoint x="${tNew.x}" y="${wy}" />`;
      }
      if (tOld && tNew && Math.abs(wx - (tOld.x + tOld.w)) < 5) {
        return `<di:waypoint x="${tNew.x + tNew.w}" y="${wy}" />`;
      }
      if (tOld && tNew && Math.abs(wx - (tOld.x + tOld.w / 2)) < 5) {
        return `<di:waypoint x="${Math.round(tNew.x + tNew.w / 2)}" y="${wy}" />`;
      }

      const newWx = Math.round(minX + (wx - minX) * scaleX);
      return `<di:waypoint x="${newWx}" y="${wy}" />`;
    });

    return `${eStart}${newContent}${eEnd}`;
  });

  return res;
}

/**
 * Rule 5 — Leftward / Loopback Flow Routing Audit (bpmn-guide.md §3B)
 *
 * For every sequence flow whose end waypoint X < start waypoint X (i.e. the flow
 * goes back to the left), checks whether the first segment moves RIGHTWARD first.
 * A right-then-left route has at least 2 unnecessary extra turns and should instead
 * exit via the Top, Bottom, or Left port for the fewest turns and least overlap.
 *
 * Logs a [Leftward-Route Warning] for each offending flow so the author knows to
 * manually reroute via an above/below-lane open channel instead.
 */
function auditLeftwardFlowRouting(xml) {
  const edgeRegex = /\u003cbpmndi:BPMNEdge\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^\u003e]*\u003e([\s\S]*?)\u003c\/bpmndi:BPMNEdge\u003e/g;
  let eMatch;
  let leftwardIssues = 0;

  while ((eMatch = edgeRegex.exec(xml)) !== null) {
    const flowId = eMatch[2];
    const content = eMatch[3];
    const waypoints = [];
    const wpRegex = /\u003cdi:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
    let wpMatch;
    while ((wpMatch = wpRegex.exec(content)) !== null) {
      waypoints.push({ x: parseFloat(wpMatch[1]), y: parseFloat(wpMatch[2]) });
    }

    if (waypoints.length < 2) continue;

    const startX = waypoints[0].x;
    const endX = waypoints[waypoints.length - 1].x;

    // Only inspect flows that travel leftward overall
    if (endX >= startX) continue;

    // Check if the first segment moves rightward (bad: unnecessary extra turns)
    const firstSegDeltaX = waypoints[1].x - waypoints[0].x;
    if (firstSegDeltaX > 5) {
      leftwardIssues++;
      const turns = waypoints.length - 2;
      console.warn(
        `[Leftward-Route Warning] Flow '${flowId}' goes LEFT (startX=${startX} → endX=${endX}) ` +
        `but first exits RIGHTWARD by ${firstSegDeltaX.toFixed(0)}px with ${turns} turn(s). ` +
        `Consider exiting via Top/Bottom/Left port through a clear above/below-lane channel for fewer turns and less overlap.`
      );
    }
  }

  if (leftwardIssues === 0) {
    console.log('[Leftward-Route Audit] Clean! All leftward/loopback flows use optimal exit ports.');
  }
}

/**
 * Rule 6 — Node Nudge-to-Align (bpmn-guide.md §2B Rule 7)
 *
 * For each sequence flow edge, if the source node's center-Y and the target node's
 * center-Y differ by at most NUDGE_THRESHOLD pixels, nudging the target node to
 * align its center-Y with the source would make the entire flow straight (0 turns,
 * 2 waypoints).
 *
 * Algorithm (multi-pass until stable):
 *  1. Parse all shape bounds into a map keyed by bpmnElement id.
 *  2. Parse all edges with their source/target bpmnElement ids.
 *  3. For each edge with 3+ waypoints (i.e. has at least 1 turn):
 *     a. Look up source center-Y and target center-Y.
 *     b. If |sourceCY - targetCY| <= NUDGE_THRESHOLD:
 *        - Compute deltaY = sourceCY - targetCY (how much to shift target).
 *        - Check that shifting target node by deltaY doesn't overlap any sibling
 *          shape in the same horizontal band (same lane, similar x range).
 *        - If safe: update target node Bounds y in the XML, update all edges
 *          connected to that node (adjust their start/end waypoint y-values),
 *          and collapse the triggering edge to 2 straight waypoints.
 *        - Log the nudge action.
 *  4. Repeat until no changes in a pass (stable).
 *
 * NUDGE_THRESHOLD: 35px — small enough to avoid major re-layouts but large enough
 * to capture near-aligned nodes that just need minor vertical correction.
 */
function nudgeNodesToStraightenFlows(xml) {
  const NUDGE_THRESHOLD = 35;
  let current = xml;
  let totalNudges = 0;
  let passNudges;

  do {
    passNudges = 0;

    // --- 1. Parse all shapes ---
    const shapes = new Map(); // bpmnElement id -> {x, y, w, h, diId, raw}
    const shapeRegex = /(<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>[\s\S]*?<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"[^/]*\/>[\s\S]*?<\/bpmndi:BPMNShape>)/g;
    let sm;
    while ((sm = shapeRegex.exec(current)) !== null) {
      const [full, , diId, elemId, sx, sy, sw, sh] = sm;
      shapes.set(elemId, {
        x: parseFloat(sx), y: parseFloat(sy),
        w: parseFloat(sw), h: parseFloat(sh),
        diId, raw: full
      });
    }

    // --- 2. Parse all edges ---
    const edges = [];
    const semanticFlowRegex = /<bpmn:sequenceFlow\s+([^>]+)>/g;
    let ef;
    while ((ef = semanticFlowRegex.exec(current)) !== null) {
      const attrs = ef[1];
      const idM = attrs.match(/id="([^"]+)"/);
      const srcM = attrs.match(/sourceRef="([^"]+)"/);
      const tgtM = attrs.match(/targetRef="([^"]+)"/);
      if (idM && srcM && tgtM) {
        edges.push({ id: idM[1], src: srcM[1], tgt: tgtM[1] });
      }
    }

    // --- 3. For each edge, check nudge eligibility ---
    for (const edge of edges) {
      const src = shapes.get(edge.src);
      const tgt = shapes.get(edge.tgt);
      if (!src || !tgt) continue;

      // Find the DI edge to count waypoints
      const diEdgeRegex = new RegExp(
        `(<bpmndi:BPMNEdge[^>]+bpmnElement="${edge.id}"[^>]*>)([\\s\\S]*?)(</bpmndi:BPMNEdge>)`
      );
      const diMatch = diEdgeRegex.exec(current);
      if (!diMatch) continue;

      const wpRegex = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
      const waypoints = [];
      let wm;
      while ((wm = wpRegex.exec(diMatch[2])) !== null) {
        waypoints.push({ x: parseFloat(wm[1]), y: parseFloat(wm[2]) });
      }
      if (waypoints.length < 3) continue; // Already straight or only 2 pts

      const srcCY = src.y + src.h / 2;
      const tgtCY = tgt.y + tgt.h / 2;
      const deltaY = srcCY - tgtCY;

      if (Math.abs(deltaY) > NUDGE_THRESHOLD) continue;
      if (Math.abs(deltaY) < 1) continue; // Already aligned

      // --- 3b. Sibling overlap check ---
      const newTgtY = tgt.y + deltaY;
      let overlaps = false;
      for (const [otherId, other] of shapes) {
        if (otherId === edge.tgt) continue;
        // Only check shapes near the same x column (within 2 node widths)
        if (Math.abs(other.x - tgt.x) > tgt.w * 2) continue;
        const overlapX = other.x < tgt.x + tgt.w && other.x + other.w > tgt.x;
        const overlapY = other.y < newTgtY + tgt.h + 10 && other.y + other.h + 10 > newTgtY;
        if (overlapX && overlapY) { overlaps = true; break; }
      }
      if (overlaps) continue;

      // --- 3c. Apply nudge: update target node Bounds y ---
      const oldBoundsStr = `<dc:Bounds x="${tgt.x}" y="${tgt.y}" width="${tgt.w}" height="${tgt.h}"`;
      const newBoundsStr = `<dc:Bounds x="${tgt.x}" y="${newTgtY.toFixed(0)}" width="${tgt.w}" height="${tgt.h}"`;
      if (!current.includes(oldBoundsStr)) continue; // safety guard
      current = current.replace(oldBoundsStr, newBoundsStr);

      // Update the shape map so subsequent passes see the new y
      tgt.y = newTgtY;

      // --- 3d. Collapse the triggering edge to 2 straight waypoints ---
      // Source exit: right port of src → target left port of tgt (or reversed)
      const srcRight = src.x + src.w;
      const tgtLeft = tgt.x;
      const straightY = Math.round(srcCY);

      let newWaypoints;
      if (srcRight <= tgtLeft) {
        // Forward flow: src right → tgt left (horizontal straight)
        newWaypoints = `        <di:waypoint x="${srcRight}" y="${straightY}" />\n        <di:waypoint x="${tgtLeft}" y="${straightY}" />`;
      } else {
        // Backward or cross flow: use centers
        newWaypoints = `        <di:waypoint x="${Math.round(src.x + src.w / 2)}" y="${straightY}" />\n        <di:waypoint x="${Math.round(tgt.x + tgt.w / 2)}" y="${straightY}" />`;
      }

      // Replace all waypoints in the DI edge
      current = current.replace(diEdgeRegex, (fullEdge, open, content, close) => {
        return `${open}\n${newWaypoints}\n      ${close}`;
      });

      // --- 3e. Also nudge all other edges anchored to the target node ---
      // Adjust their first or last waypoint y to match the new center
      const newTgtCY = Math.round(newTgtY + tgt.h / 2);
      const edgeAnchorRegex = new RegExp(
        `(<bpmndi:BPMNEdge[^>]+bpmnElement="([^"]+)"[^>]*>)([\\s\\S]*?)(</bpmndi:BPMNEdge>)`,
        'g'
      );
      current = current.replace(edgeAnchorRegex, (fullEdge, open, flowId, content, close) => {
        if (flowId === edge.id) return fullEdge; // already fixed above
        const isConnectedToTarget = (() => {
          const sfMatch = new RegExp(
            `<bpmn:sequenceFlow[^>]+id="${flowId}"[^>]*(sourceRef|targetRef)="${edge.tgt}"`
          ).test(current);
          return sfMatch;
        })();
        if (!isConnectedToTarget) return fullEdge;

        const wps = [];
        const rx = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
        let m2;
        while ((m2 = rx.exec(content)) !== null) {
          wps.push({ x: parseFloat(m2[1]), y: parseFloat(m2[2]), raw: m2[0] });
        }
        if (wps.length < 2) return fullEdge;

        // Check if first or last waypoint was the tgt node's old center
        const oldTgtCY = Math.round(srcCY - deltaY + tgt.h / 2 - tgt.h / 2 + tgt.y - deltaY + tgt.h / 2);
        // Simplified: nudge first wp if it's near old tgt bounds, or last wp
        let newContent = content;
        const firstWp = wps[0];
        const lastWp = wps[wps.length - 1];

        // Nudge last waypoint if it's the entry into the target node
        if (lastWp.x >= tgt.x - 5 && lastWp.x <= tgt.x + tgt.w + 5) {
          newContent = newContent.replace(
            lastWp.raw,
            `<di:waypoint x="${lastWp.x}" y="${newTgtCY}"`
          );
        }
        // Nudge first waypoint if it's the exit from the target node
        if (firstWp.x >= tgt.x - 5 && firstWp.x <= tgt.x + tgt.w + 5) {
          newContent = newContent.replace(
            firstWp.raw,
            `<di:waypoint x="${firstWp.x}" y="${newTgtCY}"`
          );
        }
        return `${open}${newContent}${close}`;
      });

      console.log(
        `[Nudge-to-Align] Shifted '${edge.tgt}' by ${deltaY > 0 ? '+' : ''}${Math.round(deltaY)}px Y ` +
        `to align with flow '${edge.id}' from '${edge.src}' — straightened to 2 waypoints.`
      );
      passNudges++;
      totalNudges++;
      break; // Restart pass after each nudge for accuracy
    }
  } while (passNudges > 0);

  if (totalNudges === 0) {
    console.log('[Nudge-to-Align] No nudge opportunities found — all flows already optimally routed.');
  } else {
    console.log(`[Nudge-to-Align] Complete. ${totalNudges} node(s) nudged to straighten flows.`);
  }

  return current;
}

/**
 * Same-Lane Gateway Branching (Vertical Stacking)
 * If a gateway branches to multiple target nodes in the same swimlane, 
 * places those target nodes vertically aligned in the exact same column (Center-X).
 */
function stackSameLaneGatewayBranches(xml) {
  let res = xml;

  const nodeToLane = new Map();
  const lRegex = /<bpmn:lane\s+id="([^"]+)"[^>]*>([\s\S]*?)<\/bpmn:lane>/g;
  let lm;
  while ((lm = lRegex.exec(xml)) !== null) {
    const laneId = lm[1];
    const laneContent = lm[2];
    const fnRegex = /<bpmn:flowNodeRef>([^<]+)<\/bpmn:flowNodeRef>/g;
    let fnm;
    while ((fnm = fnRegex.exec(laneContent)) !== null) {
      nodeToLane.set(fnm[1], laneId);
    }
  }

  const gwOutgoing = new Map();
  const flowMap = new Map();
  const fRegex = /<bpmn:sequenceFlow\s+([^>]+)>/g;
  let fm;
  while ((fm = fRegex.exec(xml)) !== null) {
    const attrs = fm[1];
    const idM = attrs.match(/id="([^"]+)"/);
    const srcM = attrs.match(/sourceRef="([^"]+)"/);
    const tgtM = attrs.match(/targetRef="([^"]+)"/);
    if (idM && srcM && tgtM) {
      flowMap.set(idM[1], { src: srcM[1], tgt: tgtM[1] });
      if (srcM[1].includes('Gateway') || srcM[1].includes('gw_')) {
        if (!gwOutgoing.has(srcM[1])) gwOutgoing.set(srcM[1], []);
        gwOutgoing.get(srcM[1]).push(tgtM[1]);
      }
    }
  }

  const gateways = new Set();
  const gwMatch = xml.match(/<bpmn:(?:exclusive|inclusive|parallel)Gateway\s+id="([^"]+)"/g);
  if (gwMatch) {
    gwMatch.forEach(m => {
      const id = m.match(/id="([^"]+)"/)[1];
      gateways.add(id);
    });
  }

  const shapeBounds = new Map();
  const sRegex = /<bpmndi:BPMNShape\s+id="([^"]+)_di"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"/g;
  let sm;
  while ((sm = sRegex.exec(xml)) !== null) {
    shapeBounds.set(sm[2], { x: parseFloat(sm[3]), y: parseFloat(sm[4]) });
  }

  const shapesToUpdate = new Map();

  for (const [gwId, targets] of gwOutgoing.entries()) {
    if (!gateways.has(gwId) && !gwId.toLowerCase().includes('gateway')) continue;

    const targetsByLane = new Map();
    for (const tgt of targets) {
      const laneId = nodeToLane.get(tgt);
      if (laneId) {
        if (!targetsByLane.has(laneId)) targetsByLane.set(laneId, []);
        targetsByLane.get(laneId).push(tgt);
      }
    }

    for (const [laneId, laneTargets] of targetsByLane.entries()) {
      if (laneTargets.length > 1) {
        let maxX = -Infinity;
        let minY = Infinity;
        const validTargets = [];

        for (const tgt of laneTargets) {
          const bounds = shapeBounds.get(tgt);
          if (bounds) {
            validTargets.push({ id: tgt, bounds });
            if (bounds.x > maxX) maxX = bounds.x;
            if (bounds.y < minY) minY = bounds.y;
          }
        }

        if (validTargets.length > 1) {
          validTargets.sort((a, b) => a.bounds.y - b.bounds.y);
          
          let currentY = minY;
          for (const tgtObj of validTargets) {
            shapesToUpdate.set(tgtObj.id, { x: maxX, y: currentY });
            currentY += 120; // 80px height + 40px gap
          }
        }
      }
    }
  }

  if (shapesToUpdate.size > 0) {
    let stackedCount = 0;
    const replaceRegex = /(<bpmndi:BPMNShape\s+id="[^"]+"[^>]*bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+)x="[^"]+"\s+y="[^"]+"/g;
    res = res.replace(replaceRegex, (match, prefix, bpmnElement) => {
      const update = shapesToUpdate.get(bpmnElement);
      if (update) {
        stackedCount++;
        return `${prefix}x="${update.x}" y="${update.y}"`;
      }
      return match;
    });
    
    const edgesToClear = new Set();
    for (const [flowId, flow] of flowMap.entries()) {
      if (shapesToUpdate.has(flow.src) || shapesToUpdate.has(flow.tgt)) {
        edgesToClear.add(flowId);
      }
    }

    const shapeCenters = new Map();
    for (const [id, bounds] of shapeBounds.entries()) {
      const update = shapesToUpdate.get(id);
      const b = update || bounds;
      shapeCenters.set(id, { x: b.x + 50, y: b.y + 40 });
    }

    const edgeReplaceRegex = /(<bpmndi:BPMNEdge\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>)([\s\S]*?)(<\/bpmndi:BPMNEdge>)/g;
    res = res.replace(edgeReplaceRegex, (match, openTag, edgeId, flowId, content, closeTag) => {
      if (edgesToClear.has(flowId)) {
        const flow = flowMap.get(flowId);
        if (flow) {
           const srcC = shapeCenters.get(flow.src);
           const tgtC = shapeCenters.get(flow.tgt);
           if (srcC && tgtC) {
             const wps = `\n        <di:waypoint x="${Math.round(srcC.x)}" y="${Math.round(srcC.y)}" />\n        <di:waypoint x="${Math.round(tgtC.x)}" y="${Math.round(tgtC.y)}" />`;
             const labelMatch = content.match(/<bpmndi:BPMNLabel>[\s\S]*?<\/bpmndi:BPMNLabel>/);
             const label = labelMatch ? `\n        ${labelMatch[0]}` : '';
             return `${openTag}${wps}${label}\n      ${closeTag}`;
           }
        }
      }
      return match;
    });

    if (stackedCount > 0) {
      console.log(`[Gateway Branch Stacking] Vertically stacked ${stackedCount} same-lane target nodes.`);
    }
  }

  return res;
}

/**
 * Rule 1 — Vertical Swimlane & Pool Shrink-Wrapping

 * Dynamically adjusts height and y-bounds of Swimlanes and Pools to fit contained nodes cleanly with vertical padding.
 */
function shrinkWrapSwimlanesAndPools(xml) {
  let res = xml;

  const laneNodes = new Map();
  const laneRegex = /<bpmn:lane\s+id="([^"]+)"[^>]*>([\s\S]*?)<\/bpmn:lane>/g;
  let lm;
  while ((lm = laneRegex.exec(xml)) !== null) {
    const laneId = lm[1];
    const content = lm[2];
    const nodes = new Set();
    const fnRegex = /<bpmn:flowNodeRef>([^<]+)<\/bpmn:flowNodeRef>/g;
    let fnm;
    while ((fnm = fnRegex.exec(content)) !== null) {
      nodes.add(fnm[1]);
    }
    laneNodes.set(laneId, nodes);
  }

  if (laneNodes.size === 0) return xml;

  const shapeMap = new Map();
  const sRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/g;
  let sm;
  while ((sm = sRegex.exec(xml)) !== null) {
    shapeMap.set(sm[2], { diId: sm[1], x: parseFloat(sm[3]), y: parseFloat(sm[4]), w: parseFloat(sm[5]), h: parseFloat(sm[6]) });
  }

  const V_PADDING = 25;
  let totalLaneHeight = 0;
  let currentY = null;
  const laneNewBounds = new Map();

  for (const [laneId, nodes] of laneNodes.entries()) {
    const laneShape = shapeMap.get(laneId);
    if (!laneShape) continue;

    if (currentY === null) currentY = laneShape.y;

    let minY = Infinity;
    let maxY = -Infinity;
    let maxW = laneShape.w;

    // Detect unique vertical rows/bands in swimlane
    const yBands = [];
    for (const nodeRef of nodes) {
      const nodeShape = shapeMap.get(nodeRef);
      if (nodeShape) {
        if (nodeShape.y < minY) minY = nodeShape.y;
        if (nodeShape.y + nodeShape.h > maxY) maxY = nodeShape.y + nodeShape.h;

        const nodeCY = nodeShape.y + nodeShape.h / 2;
        let matchedBand = yBands.find(b => Math.abs(b.cy - nodeCY) < 35);
        if (matchedBand) {
          matchedBand.nodes.push(nodeShape);
        } else {
          yBands.push({ cy: nodeCY, nodes: [nodeShape] });
        }
      }
    }

    const rowCount = yBands.length;
    let calculatedHeight = laneShape.h;
    if (minY !== Infinity && maxY !== -Infinity) {
      // If 2+ nodes are aligned vertically in swimlane, expand height to fit multi-row layout
      const minMultiRowHeight = rowCount >= 2 ? (rowCount * 80 + (rowCount - 1) * 40 + 60) : 120;
      const requiredHeight = Math.max(minMultiRowHeight, (maxY - minY) + V_PADDING * 2);
      calculatedHeight = Math.round(requiredHeight);

      const targetMinY = currentY + V_PADDING;
      const shiftY = Math.round(targetMinY - minY);
      if (Math.abs(shiftY) > 5) {
        for (const nodeRef of nodes) {
          const ns = shapeMap.get(nodeRef);
          if (ns) {
            const oldNodeBounds = `<dc:Bounds x="${ns.x}" y="${ns.y}" width="${ns.w}" height="${ns.h}"`;
            ns.y += shiftY;
            const newNodeBounds = `<dc:Bounds x="${ns.x}" y="${ns.y}" width="${ns.w}" height="${ns.h}"`;
            res = res.replace(oldNodeBounds, newNodeBounds);
          }
        }
      }
    }

    laneNewBounds.set(laneId, { x: laneShape.x, y: currentY, w: maxW, h: calculatedHeight });

    const oldLaneBounds = new RegExp(`(<bpmndi:BPMNShape\\s+[^>]*bpmnElement="${laneId}"[\\s\\S]*?<dc:Bounds\\s+x=")([^"]+)("\\s+y=")([^"]+)("\\s+width=")([^"]+)("\\s+height=")([^"]+)(")`);
    res = res.replace(oldLaneBounds, `$1${laneShape.x}$3${currentY}$5${maxW}$7${calculatedHeight}$9`);

    currentY += calculatedHeight;
    totalLaneHeight += calculatedHeight;
  }

  const pMatch = res.match(/<bpmn:participant\s+id="([^"]+)"/);
  if (pMatch) {
    const poolId = pMatch[1];
    const poolShape = shapeMap.get(poolId);
    if (poolShape && laneNewBounds.size > 0) {
      const firstLane = Array.from(laneNewBounds.values())[0];
      const poolY = firstLane.y;
      const oldPoolBounds = new RegExp(`(<bpmndi:BPMNShape\\s+[^>]*bpmnElement="${poolId}"[\\s\\S]*?<dc:Bounds\\s+x=")([^"]+)("\\s+y=")([^"]+)("\\s+width=")([^"]+)("\\s+height=")([^"]+)(")`);
      res = res.replace(oldPoolBounds, `$1${poolShape.x}$3${poolY}$5${poolShape.w}$7${totalLaneHeight}$9`);
      console.log(`[Vertical-ShrinkWrap] Fit ${laneNewBounds.size} Swimlanes & Pool vertically (Total Height: ${totalLaneHeight}px).`);
    }
  }

  return res;
}

/**
 * Rule 2 — Boundary Event Perimeter Alignment & Docking
 * Automatically positions <bpmn:boundaryEvent> shapes onto bottom-right perimeter of their host task.
 */
function dockBoundaryEvents(xml) {
  let res = xml;
  const boundaryMap = new Map();
  const beRegex = /<bpmn:boundaryEvent\s+id="([^"]+)"[^>]*attachedToRef="([^"]+)"/g;
  let bm;
  while ((bm = beRegex.exec(xml)) !== null) {
    boundaryMap.set(bm[1], bm[2]);
  }

  if (boundaryMap.size === 0) return xml;

  const shapes = new Map();
  const sRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/g;
  let sm;
  while ((sm = sRegex.exec(xml)) !== null) {
    shapes.set(sm[2], { x: parseFloat(sm[3]), y: parseFloat(sm[4]), w: parseFloat(sm[5]), h: parseFloat(sm[6]) });
  }

  let dockedCount = 0;
  for (const [beId, hostId] of boundaryMap.entries()) {
    const hostBounds = shapes.get(hostId);
    if (!hostBounds) continue;

    const targetX = Math.round(hostBounds.x + hostBounds.w - 20);
    const targetY = Math.round(hostBounds.y + hostBounds.h - 18);

    const oldBoundsRegex = new RegExp(`(<bpmndi:BPMNShape\\s+[^>]*bpmnElement="${beId}"[\\s\\S]*?<dc:Bounds\\s+x=")([^"]+)("\\s+y=")([^"]+)("\\s+width=")([^"]+)("\\s+height=")([^"]+)(")`);
    if (oldBoundsRegex.test(res)) {
      res = res.replace(oldBoundsRegex, `$1${targetX}$3${targetY}$536$736$9`);
      dockedCount++;
    }
  }

  if (dockedCount > 0) {
    console.log(`[Boundary-Event Docking] Successfully docked ${dockedCount} boundary event(s) to host shape perimeter.`);
  }

  return res;
}

/**
 * Rule 3 — BPMN-in-Color Standard Visual Palette
 * Applies standard OMG BPMN-in-Color attributes to shapes for visual hierarchy.
 */
function applyBpmnInColor(xml) {
  let res = xml;

  if (!res.includes('xmlns:bioc=')) {
    res = res.replace(/<bpmn:definitions\s+/, '<bpmn:definitions xmlns:bioc="http://bpmn.io/schema/bpmn/bioc/1.0" xmlns:color="http://www.omg.org/spec/BPMN/20100524/DI/color" ');
  }

  const elemTypes = new Map();
  
  const startRegex = /<bpmn:startEvent\s+id="([^"]+)"/g;
  let m;
  while ((m = startRegex.exec(xml)) !== null) elemTypes.set(m[1], 'start');

  const endRegex = /<bpmn:endEvent\s+id="([^"]+)"/g;
  while ((m = endRegex.exec(xml)) !== null) elemTypes.set(m[1], 'end');

  const gwRegex = /<bpmn:(exclusiveGateway|inclusiveGateway|parallelGateway|eventBasedGateway)\s+id="([^"]+)"/g;
  while ((m = gwRegex.exec(xml)) !== null) elemTypes.set(m[2], 'gateway');

  const taskRegex = /<bpmn:(userTask|serviceTask|sendTask|receiveTask|scriptTask|manualTask|businessRuleTask|task|subProcess|callActivity)\s+id="([^"]+)"/g;
  while ((m = taskRegex.exec(xml)) !== null) elemTypes.set(m[2], 'task');

  const palettes = {
    start: 'bioc:stroke="#2E7D32" bioc:fill="#E8F5E9" color:background-color="#E8F5E9" color:border-color="#2E7D32"',
    end: 'bioc:stroke="#C62828" bioc:fill="#FFEBEE" color:background-color="#FFEBEE" color:border-color="#C62828"',
    gateway: 'bioc:stroke="#F57F17" bioc:fill="#FFF8E1" color:background-color="#FFF8E1" color:border-color="#F57F17"',
    task: 'bioc:stroke="#1565C0" bioc:fill="#E3F2FD" color:background-color="#E3F2FD" color:border-color="#1565C0"'
  };

  let coloredCount = 0;
  res = res.replace(/<bpmndi:BPMNShape\s+([^>]+)>/g, (match, attrs) => {
    const bpmnElemMatch = attrs.match(/bpmnElement="([^"]+)"/);
    if (bpmnElemMatch && !attrs.includes('bioc:stroke')) {
      const elemId = bpmnElemMatch[1];
      const type = elemTypes.get(elemId);
      if (type && palettes[type]) {
        coloredCount++;
        return `<bpmndi:BPMNShape ${attrs} ${palettes[type]}>`;
      }
    }
    return match;
  });

  if (coloredCount > 0) {
    console.log(`[BPMN-in-Color] Applied standard visual color palette to ${coloredCount} diagram shapes.`);
  }

  return res;
}

/**
 * Rule 6 — Active Auto-Repair of Competing & Misaligned Gateway Anchor Ports
 * Snaps all Gateway sequence flow start/end waypoints to the exact outer perimeter diamond vertices (Left, Right, Top, Bottom).
 */
function repairAnchorPortDistribution(xml) {
  let res = xml;

  const shapeMap = new Map();
  const sRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/g;
  let sm;
  while ((sm = sRegex.exec(xml)) !== null) {
    const isGw = sm[1].includes('gw_') || sm[2].includes('gw_') || sm[2].includes('gateway') || sm[2].includes('Gateway');
    shapeMap.set(sm[2], { x: parseFloat(sm[3]), y: parseFloat(sm[4]), w: parseFloat(sm[5]), h: parseFloat(sm[6]), isGateway: isGw });
  }

  const flowMap = new Map();
  const fRegex = /<bpmn:sequenceFlow\s+([^>]+)>/g;
  let fm;
  while ((fm = fRegex.exec(xml)) !== null) {
    const attrs = fm[1];
    const idM = attrs.match(/id="([^"]+)"/);
    const srcM = attrs.match(/sourceRef="([^"]+)"/);
    const tgtM = attrs.match(/targetRef="([^"]+)"/);
    if (idM && srcM && tgtM) {
      flowMap.set(idM[1], { src: srcM[1], tgt: tgtM[1] });
    }
  }

  let gwFixed = 0;
  const edgeRegex = /(<bpmndi:BPMNEdge\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>)([\s\S]*?)(<\/bpmndi:BPMNEdge>)/g;

  res = res.replace(edgeRegex, (match, openTag, edgeId, flowId, content, closeTag) => {
    const flow = flowMap.get(flowId);
    if (!flow) return match;

    const waypoints = [];
    const wpRegex = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
    let wpm;
    while ((wpm = wpRegex.exec(content)) !== null) {
      waypoints.push({ x: parseFloat(wpm[1]), y: parseFloat(wpm[2]) });
    }
    if (waypoints.length < 2) return match;

    let modified = false;

    // Check Source Gateway (Start Waypoint)
    const srcShape = shapeMap.get(flow.src);
    if (srcShape && srcShape.isGateway) {
      const gwX = srcShape.x;
      const gwY = srcShape.y;
      const gwW = srcShape.w;
      const gwH = srcShape.h;

      const p1 = waypoints[0];
      const p2 = waypoints[1];
      const dx = p2.x - (gwX + gwW / 2);
      const dy = p2.y - (gwY + gwH / 2);

      let targetWp = null;
      if (Math.abs(p1.x - p2.x) <= 2) {
        // Vertical flow
        if (dy > 0) targetWp = { x: Math.round(gwX + gwW / 2), y: Math.round(gwY + gwH) };
        else targetWp = { x: Math.round(gwX + gwW / 2), y: Math.round(gwY) };
      } else if (Math.abs(p1.y - p2.y) <= 2) {
        // Horizontal flow
        if (dx > 0) targetWp = { x: Math.round(gwX + gwW), y: Math.round(gwY + gwH / 2) };
        else targetWp = { x: Math.round(gwX), y: Math.round(gwY + gwH / 2) };
      }

      if (targetWp && (Math.abs(p1.x - targetWp.x) > 1 || Math.abs(p1.y - targetWp.y) > 1)) {
        waypoints[0].x = targetWp.x;
        waypoints[0].y = targetWp.y;
        modified = true;
      }
    }

    // Check Target Gateway (End Waypoint)
    const tgtShape = shapeMap.get(flow.tgt);
    if (tgtShape && tgtShape.isGateway) {
      const gwX = tgtShape.x;
      const gwY = tgtShape.y;
      const gwW = tgtShape.w;
      const gwH = tgtShape.h;

      const lastIdx = waypoints.length - 1;
      const pLast = waypoints[lastIdx];
      const pPrev = waypoints[lastIdx - 1];
      const dx = pPrev.x - (gwX + gwW / 2);
      const dy = pPrev.y - (gwY + gwH / 2);

      let targetWp = null;
      if (Math.abs(pLast.x - pPrev.x) <= 2) {
        // Vertical entry
        if (dy > 0) targetWp = { x: Math.round(gwX + gwW / 2), y: Math.round(gwY + gwH) };
        else targetWp = { x: Math.round(gwX + gwW / 2), y: Math.round(gwY) };
      } else if (Math.abs(pLast.y - pPrev.y) <= 2) {
        // Horizontal entry
        if (dx > 0) targetWp = { x: Math.round(gwX + gwW), y: Math.round(gwY + gwH / 2) };
        else targetWp = { x: Math.round(gwX), y: Math.round(gwY + gwH / 2) };
      }

      if (targetWp && (Math.abs(pLast.x - targetWp.x) > 1 || Math.abs(pLast.y - targetWp.y) > 1)) {
        waypoints[lastIdx].x = targetWp.x;
        waypoints[lastIdx].y = targetWp.y;
        modified = true;
      }
    }

    if (modified) {
      gwFixed++;
      const newWpContent = waypoints.map(wp => `        <di:waypoint x="${Math.round(wp.x)}" y="${Math.round(wp.y)}" />`).join('\n');
      return `${openTag}\n${newWpContent}\n      ${closeTag}`;
    }

    return match;
  });

  if (gwFixed > 0) {
    console.log(`[Gateway-Anchor Auto-Fix] Aligned ${gwFixed} gateway sequence flow waypoint(s) to exact perimeter diamond vertices.`);
  }

  return res;
}

/**
 * Rule 7 — Active Rerouting of Leftward / Loopback Flows
 * Reroutes leftward flows via clear dedicated above-lane channels for 0 shape collisions and fewer turns.
 */
function rerouteLeftwardFlows(xml) {
  let res = xml;
  const shapes = new Map();
  const sRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/g;
  let sm;
  while ((sm = sRegex.exec(xml)) !== null) {
    shapes.set(sm[2], { x: parseFloat(sm[3]), y: parseFloat(sm[4]), w: parseFloat(sm[5]), h: parseFloat(sm[6]) });
  }

  const flowMap = new Map();
  const fRegex = /<bpmn:sequenceFlow\s+id="([^"]+)"\s+sourceRef="([^"]+)"\s+targetRef="([^"]+)"/g;
  let fm;
  while ((fm = fRegex.exec(xml)) !== null) {
    flowMap.set(fm[1], { src: fm[2], tgt: fm[3] });
  }

  let reroutedCount = 0;
  const edgeRegex = /(<bpmndi:BPMNEdge\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>)([\s\S]*?)(<\/bpmndi:BPMNEdge>)/g;
  
  res = res.replace(edgeRegex, (match, openTag, edgeId, flowId, content, closeTag) => {
    const flow = flowMap.get(flowId);
    if (!flow) return match;

    const srcShape = shapes.get(flow.src);
    const tgtShape = shapes.get(flow.tgt);
    if (!srcShape || !tgtShape) return match;

    if (tgtShape.x >= srcShape.x) return match;

    const waypoints = [];
    const wpRegex = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
    let wpm;
    while ((wpm = wpRegex.exec(content)) !== null) {
      waypoints.push({ x: parseFloat(wpm[1]), y: parseFloat(wpm[2]) });
    }
    if (waypoints.length < 2) return match;

    const firstDeltaX = waypoints[1].x - waypoints[0].x;
    if (firstDeltaX > 5 || waypoints.length > 4) {
      const srcCenterX = Math.round(srcShape.x + srcShape.w / 2);
      const tgtCenterX = Math.round(tgtShape.x + tgtShape.w / 2);
      const channelY = Math.round(Math.min(srcShape.y, tgtShape.y) - 30);
      
      const newWaypoints = [
        `        <di:waypoint x="${srcCenterX}" y="${Math.round(srcShape.y)}" />`,
        `        <di:waypoint x="${srcCenterX}" y="${channelY}" />`,
        `        <di:waypoint x="${tgtCenterX}" y="${channelY}" />`,
        `        <di:waypoint x="${tgtCenterX}" y="${Math.round(tgtShape.y)}" />`
      ].join('\n');

      reroutedCount++;
      return `${openTag}\n${newWaypoints}\n      ${closeTag}`;
    }

    return match;
  });

  if (reroutedCount > 0) {
    console.log(`[Leftward-Route Auto-Fix] Rerouted ${reroutedCount} loopback/leftward flow(s) via clear dedicated above-lane channels.`);
  }

  return res;
}

/**
 * Rule 9 — Enforce 100% Orthogonal Edge Routing & Shape Perimeter Touch
 * Re-calculates and snaps all edge waypoints so that start/end points touch exact shape perimeters and all segments are 100% orthogonal (0 diagonals).
 */
function enforceOrthogonalAndTouchingWaypoints(xml) {
  let res = xml;

  const shapes = new Map();
  const sRegex = /<bpmndi:BPMNShape\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>\s*<dc:Bounds\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"/g;
  let sm;
  while ((sm = sRegex.exec(res)) !== null) {
    const isGw = sm[1].includes('gw_') || sm[2].includes('gw_') || sm[2].includes('gateway') || sm[2].includes('Gateway');
    shapes.set(sm[2], { id: sm[1], elemId: sm[2], x: parseFloat(sm[3]), y: parseFloat(sm[4]), w: parseFloat(sm[5]), h: parseFloat(sm[6]), isGateway: isGw });
  }

  const flows = new Map();
  const fRegex = /<bpmn:sequenceFlow\s+([^>]+)>/g;
  let fm;
  while ((fm = fRegex.exec(res)) !== null) {
    const attrs = fm[1];
    const idM = attrs.match(/id="([^"]+)"/);
    const srcM = attrs.match(/sourceRef="([^"]+)"/);
    const tgtM = attrs.match(/targetRef="([^"]+)"/);
    if (idM && srcM && tgtM) {
      flows.set(idM[1], { src: srcM[1], tgt: tgtM[1] });
    }
  }

  function getPerimeterAnchor(shape, point) {
    const cX = Math.round(shape.x + shape.w / 2);
    const cY = Math.round(shape.y + shape.h / 2);
    const dx = point.x - cX;
    const dy = point.y - cY;

    if (shape.isGateway) {
      if (Math.abs(dx) >= Math.abs(dy)) {
        return dx >= 0 ? { x: Math.round(shape.x + shape.w), y: cY } : { x: Math.round(shape.x), y: cY };
      } else {
        return dy >= 0 ? { x: cX, y: Math.round(shape.y + shape.h) } : { x: cX, y: Math.round(shape.y) };
      }
    } else {
      if (Math.abs(dx) >= Math.abs(dy)) {
        const x = dx >= 0 ? Math.round(shape.x + shape.w) : Math.round(shape.x);
        return { x, y: cY };
      } else {
        const yVal = dy >= 0 ? Math.round(shape.y + shape.h) : Math.round(shape.y);
        return { x: cX, y: yVal };
      }
    }
  }

  let fixedEdges = 0;
  const edgeRegex = /(<bpmndi:BPMNEdge\s+id="([^"]+)"\s+bpmnElement="([^"]+)"[^>]*>)([\s\S]*?)(<\/bpmndi:BPMNEdge>)/g;

  res = res.replace(edgeRegex, (match, openTag, edgeId, flowId, content, closeTag) => {
    const flow = flows.get(flowId);
    if (!flow) return match;

    const srcShape = shapes.get(flow.src);
    const tgtShape = shapes.get(flow.tgt);
    if (!srcShape || !tgtShape) return match;

    const waypoints = [];
    const wpRegex = /<di:waypoint\s+x="([^"]+)"\s+y="([^"]+)"/g;
    let wpm;
    while ((wpm = wpRegex.exec(content)) !== null) {
      waypoints.push({ x: parseFloat(wpm[1]), y: parseFloat(wpm[2]) });
    }
    if (waypoints.length < 2) return match;

    waypoints[0] = getPerimeterAnchor(srcShape, waypoints[1]);
    waypoints[waypoints.length - 1] = getPerimeterAnchor(tgtShape, waypoints[waypoints.length - 2]);

    const orthogonalWaypoints = [waypoints[0]];
    for (let i = 1; i < waypoints.length; i++) {
      const pPrev = orthogonalWaypoints[orthogonalWaypoints.length - 1];
      const pCurr = waypoints[i];

      if (Math.abs(pPrev.x - pCurr.x) > 1 && Math.abs(pPrev.y - pCurr.y) > 1) {
        if (i === waypoints.length - 1) {
          if (pCurr.x === waypoints[waypoints.length - 1].x) {
            orthogonalWaypoints.push({ x: Math.round(pCurr.x), y: Math.round(pPrev.y) });
          } else {
            orthogonalWaypoints.push({ x: Math.round(pPrev.x), y: Math.round(pCurr.y) });
          }
        } else {
          orthogonalWaypoints.push({ x: Math.round(pCurr.x), y: Math.round(pPrev.y) });
        }
      }
      orthogonalWaypoints.push({ x: Math.round(pCurr.x), y: Math.round(pCurr.y) });
    }

    const cleanWaypoints = [orthogonalWaypoints[0]];
    for (let i = 1; i < orthogonalWaypoints.length; i++) {
      const pLast = cleanWaypoints[cleanWaypoints.length - 1];
      const pNext = orthogonalWaypoints[i];
      if (Math.abs(pLast.x - pNext.x) <= 1 && Math.abs(pLast.y - pNext.y) <= 1) continue;

      if (cleanWaypoints.length >= 2) {
        const pSecondLast = cleanWaypoints[cleanWaypoints.length - 2];
        if (Math.abs(pSecondLast.x - pLast.x) <= 1 && Math.abs(pLast.x - pNext.x) <= 1) {
          cleanWaypoints.pop();
        } else if (Math.abs(pSecondLast.y - pLast.y) <= 1 && Math.abs(pLast.y - pNext.y) <= 1) {
          cleanWaypoints.pop();
        }
      }
      cleanWaypoints.push(pNext);
    }

    cleanWaypoints[0] = getPerimeterAnchor(srcShape, cleanWaypoints[1]);
    cleanWaypoints[cleanWaypoints.length - 1] = getPerimeterAnchor(tgtShape, cleanWaypoints[cleanWaypoints.length - 2]);

    const newWpXml = cleanWaypoints.map(wp => `        <di:waypoint x="${Math.round(wp.x)}" y="${Math.round(wp.y)}" />`).join('\n');
    fixedEdges++;
    return `${openTag}\n${newWpXml}\n      ${closeTag}`;
  });

  if (fixedEdges > 0) {
    console.log(`[Orthogonal & Perimeter Repair] Enforced strict 100% orthogonal routing and shape perimeter touching on ${fixedEdges} sequence flow edges.`);
  }

  return res;
}

/**
 * Strips invalid semantic attributes (like 'name') from visual DI elements
 * which causes schema validation errors in downstream linters.
 */
function stripInvalidDiAttributes(xml) {
  let res = xml;
  // Remove name="..." from <bpmndi:BPMNEdge ...> and <bpmndi:BPMNShape ...>
  let strippedCount = 0;
  res = res.replace(/(<bpmndi:BPMN(?:Edge|Shape)\s+[^>]*?)(\s+name="[^"]*")/g, (match, p1, p2) => {
    strippedCount++;
    return p1;
  });
  if (strippedCount > 0) {
    console.log(`[Schema Auto-Fix] Stripped invalid 'name' attribute from ${strippedCount} DI element(s).`);
  }
  return res;
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

main();

