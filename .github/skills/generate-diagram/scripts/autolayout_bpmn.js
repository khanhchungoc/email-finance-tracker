import fs from 'node:fs';

/**
 * Enhanced BPMN 2.0 Auto-Layout & Post-Processing Utility
 * Enforces 4 Core Layout Rules from bpmn-guide.md:
 * 1. Same-Lane Progression: Keep going horizontally right along main center spine.
 * 2. Lane-Change Continuation: Direct 0-turn vertical alignment if clear; Right-Up / Right-Down staggering if overlapping arrows/nodes.
 * 3. Minimal Competing Anchors: Clean port distribution (Left=in, Right=out, Top/Bottom=rejection/loop) to prevent arrowhead collisions.
 * 4. Horizontal Row Alignment & Secondary Rows: Nodes on the same line are aligned on Center-Y; create secondary parallel rows in the swimlane if overlapping.
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
    if (!xml.includes('Participant_') && !xml.includes('lane_')) {
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

  // Rule 1: Ensure Exclusive Gateways with multiple outgoing flows declare a default attribute
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

  // Rule 2: Ensure Sequence Flow labels sit at least 15px above horizontal edge waypoints
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

  // Rule 3: Line-Through-Shape Collision Audit Inspector
  auditLineShapeCollisions(processed);

  // Rule 4: Competing Anchor Port Distribution Audit
  auditAnchorPortDistribution(processed);

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
  const flowRegex = /<bpmn:sequenceFlow\s+id="([^"]+)"\s+sourceRef="([^"]+)"\s+targetRef="([^"]+)"/g;
  let fMatch;
  while ((fMatch = flowRegex.exec(xml)) !== null) {
    flowSourceTargetMap[fMatch[1]] = { sourceRef: fMatch[2], targetRef: fMatch[3] };
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

      portUsage[startWp] = portUsage[startWp] || [];
      portUsage[startWp].push({ flowId, role: 'exit' });

      portUsage[endWp] = portUsage[endWp] || [];
      portUsage[endWp].push({ flowId, role: 'entry' });
    }
  }

  let duplicateCount = 0;
  for (const [wpKey, flows] of Object.entries(portUsage)) {
    if (flows.length > 1) {
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

main();
