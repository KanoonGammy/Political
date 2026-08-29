// Thai Politics Semantic Graph Dashboard Controller

let network = null;
let allNodes = [];
let allEdges = [];
let nodesDataSet = null;
let edgesDataSet = null;
let currentPartyFilter = 'all';
let currentRelFilter = 'ALL';
let currentTimelineDays = 30;
let physicsEnabled = true;

// Color Palette Mapping
const COALITION_COLORS = {
  "พรรคเพื่อไทย": { bg: "#ef4444", border: "#b91c1c", highlight: "#f87171" },
  "พรรคประชาชน": { bg: "#f97316", border: "#c2410c", highlight: "#fb923c" },
  "พรรคภูมิใจไทย": { bg: "#2563eb", border: "#1d4ed8", highlight: "#60a5fa" },
  "พรรครวมไทยสร้างชาติ": { bg: "#3b82f6", border: "#1d4ed8", highlight: "#93c5fd" },
  "พรรคประชาธิปัตย์": { bg: "#06b6d4", border: "#0e7490", highlight: "#67e8f9" },
  "พรรคพลังประชารัฐ": { bg: "#10b981", border: "#047857", highlight: "#34d399" },
  "พรรคพลังประชารัฐ (กลุ่มธรรมนัส)": { bg: "#10b981", border: "#047857", highlight: "#34d399" },
  "Government": { bg: "#ef4444", border: "#b91c1c", highlight: "#f87171" },
  "Opposition": { bg: "#f97316", border: "#c2410c", highlight: "#fb923c" },
  "Independent": { bg: "#8b5cf6", border: "#6d28d9", highlight: "#a78bfa" },
  "Judicial": { bg: "#a855f7", border: "#7e22ce", highlight: "#c084fc" },
  "Cross-Party": { bg: "#ec4899", border: "#be185d", highlight: "#f472b6" }
};

const RELATION_COLORS = {
  "ALLIANCE": { color: "#10b981", highlight: "#34d399", hover: "#059669" },
  "OPPOSITION": { color: "#ef4444", highlight: "#f87171", hover: "#dc2626" },
  "CRITICISM": { color: "#f59e0b", highlight: "#fbbf24", hover: "#d97706" },
  "LEGAL_ACTION": { color: "#8b5cf6", highlight: "#a78bfa", hover: "#7c3aed" },
  "MEMBER_OF": { color: "#64748b", highlight: "#94a3b8", hover: "#475569" },
  "INVESTIGATION": { color: "#ec4899", highlight: "#f472b6", hover: "#db2777" },
  "POLICY_STANCE": { color: "#06b6d4", highlight: "#67e8f9", hover: "#0891b2" }
};

async function initDashboard() {
  try {
    let graphData = null;
    const candidatePaths = [
      'data/graph_data.json',
      './data/graph_data.json',
      '../data/graph_data.json',
      '/Political/data/graph_data.json',
      '/data/graph_data.json'
    ];

    for (const p of candidatePaths) {
      try {
        const res = await fetch(p);
        if (res.ok) {
          graphData = await res.json();
          console.log(`[OK] Loaded graph data from ${p}`);
          break;
        }
      } catch (e) {}
    }

    if (!graphData) {
      throw new Error("Could not load data/graph_data.json from any candidate paths");
    }

    allNodes = graphData.nodes || [];
    allEdges = graphData.edges || [];

    // Update Header Stats
    document.getElementById('stat-nodes').textContent = allNodes.length;
    document.getElementById('stat-edges').textContent = allEdges.length;
    document.getElementById('stat-articles').textContent = graphData.metadata?.articles_analyzed || 0;

    renderGraph();
    setupEventListeners();
  } catch (err) {
    console.error("Dashboard initialization error:", err);
    document.getElementById('drawer-body').innerHTML = `
      <div class="dossier-card" style="border-color:#ef4444;">
        <h4 style="color:#ef4444;">เกิดข้อผิดพลาดในการโหลดข้อมูล</h4>
        <p style="font-size:0.85rem; margin-top:6px;">กรุณาตรวจสอบว่ามีไฟล์ <code>data/graph_data.json</code> หรือเปิดผ่าน local web server</p>
      </div>
    `;
  }
}

function getNodeColor(node) {
  if (node.party && COALITION_COLORS[node.party]) {
    return COALITION_COLORS[node.party];
  }
  if (node.coalition && COALITION_COLORS[node.coalition]) {
    return COALITION_COLORS[node.coalition];
  }
  return { bg: "#3b82f6", border: "#1d4ed8", highlight: "#60a5fa" };
}

function renderGraph() {
  const container = document.getElementById('graph-canvas');

  // Filter nodes based on active filters
  const filteredNodes = allNodes.filter(node => {
    if (currentPartyFilter === 'all') return true;
    return node.coalition === currentPartyFilter || node.party === currentPartyFilter;
  });

  const activeNodeIds = new Set(filteredNodes.map(n => n.id));

  // Filter edges based on active nodes and relation type
  const filteredEdges = allEdges.filter(edge => {
    if (!activeNodeIds.has(edge.source) || !activeNodeIds.has(edge.target)) return false;
    if (currentRelFilter !== 'ALL' && edge.relation_type !== currentRelFilter) return false;
    return true;
  });

  // Prepare Vis.js datasets
  const visNodes = filteredNodes.map(node => {
    const colorStyle = getNodeColor(node);
    const size = Math.min(45, Math.max(22, 18 + (node.mention_count || 1) * 1.5));
    
    return {
      id: node.id,
      label: node.name,
      title: `${node.name}\nตำแหน่ง: ${node.role || '-'}\nสังกัด: ${node.party || '-'}\nปรากฏในข่าว: ${node.mention_count} ครั้ง`,
      shape: node.type === 'INSTITUTION' ? 'box' : (node.type === 'PARTY' ? 'diamond' : 'dot'),
      size: size,
      color: {
        background: colorStyle.bg,
        border: colorStyle.border,
        highlight: {
          background: colorStyle.highlight,
          border: "#ffffff"
        }
      },
      font: {
        color: '#ffffff',
        size: 13,
        face: 'Noto Sans Thai, Inter',
        strokeWidth: 3,
        strokeColor: '#0b0f19'
      },
      borderWidth: 2,
      shadow: { enabled: true, color: 'rgba(0,0,0,0.6)', size: 8, x: 2, y: 2 },
      raw: node
    };
  });

  const visEdges = filteredEdges.map(edge => {
    const relColor = RELATION_COLORS[edge.relation_type] || { color: "#9ca3af", highlight: "#ffffff" };
    const isDashed = edge.relation_type === 'LEGAL_ACTION' || edge.relation_type === 'CRITICISM';

    return {
      id: edge.id,
      from: edge.source,
      to: edge.target,
      label: edge.relation_type.replace('_', ' '),
      title: `ความสัมพันธ์: ${edge.description}\nหลักฐาน: "${edge.evidence}"`,
      arrows: {
        to: { enabled: true, scaleFactor: 0.6 }
      },
      color: {
        color: relColor.color,
        highlight: relColor.highlight,
        hover: relColor.hover
      },
      dashes: isDashed,
      width: Math.min(6, Math.max(1.5, edge.weight * 1.2)),
      font: {
        color: '#d1d5db',
        size: 9,
        align: 'middle',
        strokeWidth: 2,
        strokeColor: '#0b0f19'
      },
      smooth: {
        type: 'continuous',
        roundness: 0.2
      },
      raw: edge
    };
  });

  nodesDataSet = new vis.DataSet(visNodes);
  edgesDataSet = new vis.DataSet(visEdges);

  const data = { nodes: nodesDataSet, edges: edgesDataSet };

  const options = {
    nodes: {
      scaling: { min: 16, max: 40 }
    },
    edges: {
      selectionWidth: 3,
      hoverWidth: 2
    },
    physics: {
      enabled: physicsEnabled,
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -70,
        centralGravity: 0.015,
        springLength: 120,
        springConstant: 0.08,
        damping: 0.4
      },
      stabilization: { iterations: 150 }
    },
    interaction: {
      hover: true,
      tooltipDelay: 150,
      navigationButtons: false,
      keyboard: true
    }
  };

  network = new vis.Network(container, data, options);

  // Click handler
  network.on('click', function(params) {
    if (params.nodes.length > 0) {
      const selectedNodeId = params.nodes[0];
      const nodeObj = allNodes.find(n => n.id === selectedNodeId);
      if (nodeObj) showNodeDossier(nodeObj);
    } else if (params.edges.length > 0) {
      const selectedEdgeId = params.edges[0];
      const edgeObj = allEdges.find(e => e.id === selectedEdgeId);
      if (edgeObj) showEdgeDossier(edgeObj);
    }
  });
}

function showNodeDossier(node) {
  const drawer = document.getElementById('evidence-drawer');
  const title = document.getElementById('drawer-title');
  const body = document.getElementById('drawer-body');

  title.textContent = node.name;

  // Find all connected edges
  const connectedEdges = allEdges.filter(e => e.source === node.id || e.target === node.id);

  let relationsHtml = connectedEdges.map(e => {
    const otherId = e.source === node.id ? e.target : e.source;
    const otherNode = allNodes.find(n => n.id === otherId);
    const otherName = otherNode ? otherNode.name : otherId;
    const relColor = (RELATION_COLORS[e.relation_type] || {}).color || "#3b82f6";

    return `
      <div class="relation-item" style="border-left-color:${relColor};">
        <div style="display:flex; justify-content:space-between; font-weight:600;">
          <span>${e.relation_type} ➔ ${otherName}</span>
          <span style="font-size:0.75rem; color:var(--text-muted);">${e.date}</span>
        </div>
        <p style="margin-top:4px;">${e.description}</p>
        <div class="evidence-quote">"${e.evidence}"</div>
        ${e.source_url ? `<a href="${e.source_url}" target="_blank" style="font-size:0.75rem; color:var(--accent-primary); display:inline-block; margin-top:4px;">🔗 แหล่งข่าวอ้างอิง</a>` : ''}
      </div>
    `;
  }).join('');

  body.innerHTML = `
    <div class="dossier-card">
      <div style="font-size:0.8rem; text-transform:uppercase; color:var(--text-muted);">บทบาท / ตำแหน่ง</div>
      <div style="font-size:1.05rem; font-weight:600; margin-top:2px;">${node.role || 'ไม่มีระบุ'}</div>
      <div style="margin-top:8px; display:flex; gap:8px;">
        <span class="stat-badge" style="font-size:0.75rem;">สังกัด: ${node.party || 'อิสระ'}</span>
        <span class="stat-badge" style="font-size:0.75rem;">ขั้ว: ${node.coalition || '-'}</span>
      </div>
      <div style="margin-top:10px; font-size:0.8rem; color:var(--text-muted);">
        ความถี่ในข่าวรอบ 30 วัน: <strong style="color:var(--accent-primary);">${node.mention_count}</strong> ครั้ง
      </div>
      ${node.wiki_link ? `<div style="margin-top:8px; font-size:0.8rem;"><a href="../wiki/entities/${node.id}.md" target="_blank" style="color:var(--accent-primary);">📖 ดูเอกสารสรุปใน LLM-Wiki</a></div>` : ''}
    </div>

    <h3 style="font-size:0.9rem; margin-top:8px;">โครงข่ายความสัมพันธ์ที่เกี่ยวข้อง (${connectedEdges.length})</h3>
    ${relationsHtml || '<p style="font-size:0.8rem; color:var(--text-muted);">ยังไม่มีความสัมพันธ์ที่บันทึกไว้</p>'}
  `;

  drawer.classList.add('open');
}

function showEdgeDossier(edge) {
  const drawer = document.getElementById('evidence-drawer');
  const title = document.getElementById('drawer-title');
  const body = document.getElementById('drawer-body');

  const srcNode = allNodes.find(n => n.id === edge.source);
  const tgtNode = allNodes.find(n => n.id === edge.target);

  title.textContent = `ความสัมพันธ์: ${edge.relation_type}`;

  body.innerHTML = `
    <div class="dossier-card">
      <div style="font-size:1rem; font-weight:600;">
        ${srcNode ? srcNode.name : edge.source} ➔ ${tgtNode ? tgtNode.name : edge.target}
      </div>
      <p style="margin-top:8px; font-size:0.88rem;">${edge.description}</p>
      <div style="margin-top:8px; font-size:0.78rem; color:var(--text-muted);">
        วันที่บันทึก: ${edge.date} | ความถี่ซ้ำ: ${edge.weight}
      </div>
    </div>

    <h3 style="font-size:0.9rem; margin-top:8px;">ข้อความหลักฐานจากข่าว (Evidence)</h3>
    <div class="evidence-quote" style="font-size:0.88rem; line-height:1.5;">
      "${edge.evidence}"
    </div>

    ${edge.source_url ? `
      <div style="margin-top:12px;">
        <a href="${edge.source_url}" target="_blank" class="tool-btn" style="text-decoration:none; justify-content:center;">
          🌐 เปิดอ่านข่าวต้นฉบับ
        </a>
      </div>
    ` : ''}
  `;

  drawer.classList.add('open');
}

function setupEventListeners() {
  // Close drawer
  document.getElementById('drawer-close').addEventListener('click', () => {
    document.getElementById('evidence-drawer').classList.remove('open');
  });

  // Party Filter Buttons
  document.querySelectorAll('#party-filters .filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#party-filters .filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentPartyFilter = btn.getAttribute('data-filter');
      renderGraph();
    });
  });

  // Relation Filter Buttons
  document.querySelectorAll('#relation-filters .filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#relation-filters .filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentRelFilter = btn.getAttribute('data-rel');
      renderGraph();
    });
  });

  // Search Input
  document.getElementById('search-input').addEventListener('input', (e) => {
    const val = e.target.value.trim().toLowerCase();
    if (!val || !network) return;

    const matched = allNodes.find(n => 
      n.name.toLowerCase().includes(val) || 
      (n.aliases && n.aliases.some(a => a.toLowerCase().includes(val)))
    );

    if (matched) {
      network.focus(matched.id, {
        scale: 1.2,
        animation: { duration: 600, easingFunction: 'easeInOutQuad' }
      });
      network.selectNodes([matched.id]);
      showNodeDossier(matched);
    }
  });

  // Fit View
  document.getElementById('btn-fit').addEventListener('click', () => {
    if (network) network.fit({ animation: { duration: 500 } });
  });

  // Reload
  document.getElementById('btn-refresh').addEventListener('click', () => {
    initDashboard();
  });

  // Physics Toggle
  document.getElementById('toggle-physics').addEventListener('click', (e) => {
    physicsEnabled = !physicsEnabled;
    if (network) network.setOptions({ physics: { enabled: physicsEnabled } });
    e.currentTarget.innerHTML = physicsEnabled ? 
      '<span>🔒 ตรึงตำแหน่งกราฟ (Lock Physics)</span>' : 
      '<span>⚡ คลายแรงฟิสิกส์ (Unlock Physics)</span>';
  });
}

document.addEventListener('DOMContentLoaded', initDashboard);
