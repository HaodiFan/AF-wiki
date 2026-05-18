const repoRoot = "https://github.com/HaodiFan/AF-wiki/blob/main/";

const colors = {
  green: "#66d37e",
  teal: "#3dd6c6",
  blue: "#77a7ff",
  orange: "#ffb454",
  red: "#ff6b5d",
  gold: "#e6c55a",
};

const data = {
  fitness: {
    metrics: [
      { value: "11", label: "indexed days", note: "days table, 2026-04 window" },
      { value: "8", label: "training sessions", note: "5 strength + 3 swim" },
      { value: "273.5", label: "logged minutes", note: "184.0 strength + 89.5 swim" },
      { value: "1,968", label: "logged kcal", note: "from sessions with summary metrics" },
    ],
    sessionTotals: [
      { label: "Strength", sessions: 5, minutes: 184.0, kcal: 1429, color: colors.green },
      { label: "Swim", sessions: 3, minutes: 89.5, kcal: 539, color: colors.teal },
    ],
    timeline: [
      { date: "04-18", type: "Swim", label: "aerobic swim", meta: "26.7 min · 180 kcal · avg HR 150", color: colors.teal },
      { date: "04-20", type: "Strength", label: "chest + triceps + core", meta: "48.5 min · 414 kcal · avg HR 128", color: colors.green },
      { date: "04-21", type: "Strength", label: "back + biceps substitute pull day", meta: "42.3 min · 335 kcal · avg HR 123", color: colors.green },
      { date: "04-22", type: "Swim", label: "moderate aerobic swim", meta: "23.8 min · 141 kcal · avg HR 133", color: colors.teal },
      { date: "04-25", type: "Strength", label: "shoulders + arms + core", meta: "42.6 min · 361 kcal · avg HR 126", color: colors.green },
      { date: "04-26", type: "Swim", label: "aerobic swim", meta: "39.0 min · 218 kcal · avg HR 132", color: colors.teal },
      { date: "04-27", type: "Strength", label: "chest + triceps + core", meta: "50.6 min · 319 kcal · avg HR 111", color: colors.green },
      { date: "04-28", type: "Strength", label: "back + biceps machine session", meta: "exercise details logged; summary metrics pending", color: colors.green },
    ],
    strengths: [
      { label: "Bench press", value: 60, detail: "60 x 5", color: colors.red },
      { label: "Lat pulldown", value: 55, detail: "55 x 8-12", color: colors.blue },
      { label: "Seated row", value: 45, detail: "45 x 12", color: colors.teal },
      { label: "Incline press", value: 40, detail: "40 x 10", color: colors.orange },
      { label: "Chest press", value: 30, detail: "30 x 12", color: colors.green },
      { label: "Ab machine", value: 52.5, detail: "52.5 x 12", color: colors.gold },
    ],
  },
  knowledge: {
    metrics: [
      { value: "18", label: "topic nodes", note: "durable concepts in areas/knowledge/topics" },
      { value: "1", label: "curated map", note: "Agent Systems Map" },
      { value: "5", label: "research notes", note: "resources/research" },
      { value: "139", label: "source refs", note: "manifest counts across 3 source families" },
    ],
    pipeline: [
      { label: "Lead", count: 9, note: "weak signals and candidates", color: colors.orange },
      { label: "Research", count: 5, note: "investigated notes and provisional verdicts", color: colors.blue },
      { label: "Topic", count: 18, note: "reusable durable nodes", color: colors.green },
      { label: "Map", count: 1, note: "curated graph entry point", color: colors.teal },
    ],
    topics: [
      { label: "Large Language Models", cn: "大语言模型", group: "model", href: "areas/knowledge/topics/large-language-models.md" },
      { label: "Multimodal AI", cn: "多模态 AI", group: "model", href: "areas/knowledge/topics/multimodal-ai.md" },
      { label: "AI4Science", cn: "AI4Science", group: "model", href: "areas/knowledge/topics/ai4science.md" },
      { label: "Quantum Computing", cn: "量子计算", group: "model", href: "areas/knowledge/topics/quantum-computing.md" },
      { label: "Agent Core", cn: "智能体核心", group: "agent", href: "areas/knowledge/topics/agent-core.md" },
      { label: "Agent Memory", cn: "智能体记忆", group: "agent", href: "areas/knowledge/topics/agent-memory.md" },
      { label: "Agent Runtime", cn: "智能体运行时", group: "agent", href: "areas/knowledge/topics/agent-runtime.md" },
      { label: "Agent Harness Engineering", cn: "智能体 Harness Engineering", group: "agent", href: "areas/knowledge/topics/agent-harness-engineering.md" },
      { label: "Function Calling and Tool Use", cn: "函数调用与工具使用", group: "interface", href: "areas/knowledge/topics/function-calling-and-tool-use.md" },
      { label: "Workflow Runtime", cn: "工作流运行时", group: "interface", href: "areas/knowledge/topics/workflow-runtime.md" },
      { label: "Ontology", cn: "本体", group: "interface", href: "areas/knowledge/topics/ontology.md" },
      { label: "Data Management", cn: "数据管理", group: "interface", href: "areas/knowledge/topics/data-management.md" },
      { label: "LLM Safety and Interpretability", cn: "LLM 安全与可解释性", group: "governance", href: "areas/knowledge/topics/llm-safety-interpretability.md" },
      { label: "Self-Evolving AI Systems", cn: "自演化 AI 系统", group: "governance", href: "areas/knowledge/topics/self-evolving-ai-systems.md" },
      { label: "OpenClaw", cn: "OpenClaw", group: "reference", href: "areas/knowledge/topics/openclaw.md" },
      { label: "NanoClaw / Nanobot", cn: "NanoClaw / Nanobot", group: "reference", href: "areas/knowledge/topics/nanoclaw.md" },
      { label: "Opencode Architecture", cn: "Opencode 架构", group: "reference", href: "areas/knowledge/topics/opencode-architecture.md" },
      { label: "Wire Harness Engineering", cn: "线束工程", group: "reference", href: "areas/knowledge/topics/wire-harness-engineering.md" },
    ],
    graphNodes: [
      { id: "llm", label: "LLM", sub: "model substrate", x: 70, y: 220, color: colors.blue },
      { id: "core", label: "Agent Core", sub: "control loop", x: 260, y: 120, color: colors.green },
      { id: "memory", label: "Memory", sub: "durable state", x: 260, y: 250, color: colors.green },
      { id: "runtime", label: "Runtime", sub: "tools + sessions", x: 260, y: 380, color: colors.green },
      { id: "harness", label: "Harness", sub: "evals + rules", x: 470, y: 120, color: colors.orange },
      { id: "ontology", label: "Ontology", sub: "world model", x: 470, y: 250, color: colors.teal },
      { id: "workflow", label: "Workflow", sub: "executable flow", x: 470, y: 380, color: colors.teal },
      { id: "safety", label: "Safety", sub: "evidence constraints", x: 680, y: 120, color: colors.red },
      { id: "self", label: "Self-evolving", sub: "feedback loops", x: 680, y: 250, color: colors.gold },
      { id: "refs", label: "Reference systems", sub: "OpenClaw / NanoClaw", x: 680, y: 380, color: colors.blue },
    ],
    graphEdges: [
      ["llm", "core"],
      ["llm", "memory"],
      ["llm", "runtime"],
      ["core", "harness"],
      ["memory", "ontology"],
      ["runtime", "workflow"],
      ["harness", "safety"],
      ["harness", "self"],
      ["ontology", "self"],
      ["workflow", "refs"],
      ["runtime", "refs"],
    ],
  },
};

const groupLabels = {
  all: "All",
  model: "Model",
  agent: "Agent",
  interface: "Interface",
  governance: "Governance",
  reference: "Reference",
};

const groupColors = {
  model: colors.blue,
  agent: colors.green,
  interface: colors.teal,
  governance: colors.gold,
  reference: colors.orange,
};

function createMetric(metric) {
  const article = document.createElement("article");
  article.className = "metric";
  article.innerHTML = `<strong>${metric.value}</strong><span>${metric.label}</span><small>${metric.note}</small>`;
  return article;
}

function renderMetrics(targetId, metrics) {
  const target = document.getElementById(targetId);
  target.replaceChildren(...metrics.map(createMetric));
}

function renderSessionBars() {
  const maxMinutes = Math.max(...data.fitness.sessionTotals.map((item) => item.minutes));
  const rows = data.fitness.sessionTotals.map((item) => {
    const row = document.createElement("div");
    row.className = "bar-row";
    const width = `${Math.round((item.minutes / maxMinutes) * 100)}%`;
    row.innerHTML = `
      <span class="bar-label">${item.label}</span>
      <span class="bar-track"><span class="bar-fill" style="width:${width};background:${item.color}"></span></span>
      <span class="bar-value">${item.sessions} · ${item.minutes}m</span>
    `;
    return row;
  });
  document.getElementById("sessionBars").replaceChildren(...rows);
}

function renderTimeline() {
  const items = data.fitness.timeline.map((item) => {
    const node = document.createElement("div");
    node.className = "timeline-item";
    node.innerHTML = `
      <span class="timeline-date">${item.date}</span>
      <span class="timeline-dot" style="background:${item.color}"></span>
      <span class="timeline-copy"><strong>${item.type} · ${item.label}</strong><span>${item.meta}</span></span>
    `;
    return node;
  });
  document.getElementById("sessionTimeline").replaceChildren(...items);
}

function renderStrengthChart() {
  const maxValue = Math.max(...data.fitness.strengths.map((item) => item.value));
  const rows = data.fitness.strengths.map((item) => {
    const row = document.createElement("div");
    row.className = "strength-row";
    const width = `${Math.round((item.value / maxValue) * 100)}%`;
    row.innerHTML = `
      <span class="strength-label">${item.label}</span>
      <span class="strength-track"><span class="strength-fill" style="width:${width};background:${item.color}"></span></span>
      <span class="strength-value">${item.detail}</span>
    `;
    return row;
  });
  document.getElementById("strengthChart").replaceChildren(...rows);
}

function renderPipeline() {
  const steps = data.knowledge.pipeline.map((step) => {
    const node = document.createElement("article");
    node.className = "pipeline-step";
    node.style.borderTop = `6px solid ${step.color}`;
    node.innerHTML = `<strong>${step.count}</strong><h4>${step.label}</h4><p>${step.note}</p>`;
    return node;
  });
  document.getElementById("knowledgePipeline").replaceChildren(...steps);
}

function renderGraph() {
  const nodesById = new Map(data.knowledge.graphNodes.map((node) => [node.id, node]));
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 860 520");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", "Agent systems topic graph");

  data.knowledge.graphEdges.forEach(([fromId, toId]) => {
    const from = nodesById.get(fromId);
    const to = nodesById.get(toId);
    const line = document.createElementNS(svg.namespaceURI, "line");
    line.setAttribute("x1", from.x + 112);
    line.setAttribute("y1", from.y + 44);
    line.setAttribute("x2", to.x);
    line.setAttribute("y2", to.y + 44);
    line.setAttribute("class", "graph-edge");
    svg.appendChild(line);
  });

  data.knowledge.graphNodes.forEach((node) => {
    const group = document.createElementNS(svg.namespaceURI, "g");
    group.setAttribute("class", "graph-node");
    group.setAttribute("transform", `translate(${node.x}, ${node.y})`);

    const rect = document.createElementNS(svg.namespaceURI, "rect");
    rect.setAttribute("width", "150");
    rect.setAttribute("height", "88");
    rect.setAttribute("stroke", node.color);

    const label = document.createElementNS(svg.namespaceURI, "text");
    label.setAttribute("x", "18");
    label.setAttribute("y", "36");
    label.textContent = node.label;

    const sub = document.createElementNS(svg.namespaceURI, "text");
    sub.setAttribute("x", "18");
    sub.setAttribute("y", "60");
    sub.setAttribute("class", "subtext");
    sub.textContent = node.sub;

    group.append(rect, label, sub);
    svg.appendChild(group);
  });

  document.getElementById("agentGraph").replaceChildren(svg);
}

function renderTopicFilters(activeGroup = "all") {
  const groups = ["all", "model", "agent", "interface", "governance", "reference"];
  const buttons = groups.map((group) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = groupLabels[group];
    button.setAttribute("aria-pressed", String(group === activeGroup));
    button.addEventListener("click", () => {
      renderTopicFilters(group);
      renderTopicGrid(group);
    });
    return button;
  });
  document.getElementById("topicFilters").replaceChildren(...buttons);
}

function renderTopicGrid(group = "all") {
  const topics = group === "all" ? data.knowledge.topics : data.knowledge.topics.filter((topic) => topic.group === group);
  const cards = topics.map((topic) => {
    const article = document.createElement("article");
    article.className = "topic-card";
    article.style.borderLeftColor = groupColors[topic.group];
    article.innerHTML = `
      <a href="${repoRoot}${topic.href}">${topic.label}</a>
      <span>${topic.cn} · ${groupLabels[topic.group]}</span>
    `;
    return article;
  });
  document.getElementById("topicGrid").replaceChildren(...cards);
}

renderMetrics("fitnessMetrics", data.fitness.metrics);
renderMetrics("knowledgeMetrics", data.knowledge.metrics);
renderSessionBars();
renderTimeline();
renderStrengthChart();
renderPipeline();
renderGraph();
renderTopicFilters();
renderTopicGrid();
