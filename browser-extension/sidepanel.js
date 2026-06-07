const GUARDRAIL_NOTE = `> **Artificial Wisdom Guardrail Note**  
> This repository or page is interpreted through the six principles of Natural Law: Natural Law, Harmony, Circulation, Structure, Order, and Wa.  
> The purpose is not domination of nature, but restoration of natural cycles through measurable, cautious, and open human-AI co-creation.  
>  
> This note is a conceptual and ethical framing, not a claim of scientific proof, certification, or completed implementation.`;

const PRINCIPLES = [
  {
    key: "naturalLaw",
    label: "Natural Law / 自然法則",
    keywords: ["natural law", "nature", "natural", "ecology", "ecosystem", "climate", "soil", "ocean", "rain", "water", "自然", "自然法則", "生態", "気候", "土壌", "海洋", "雨", "水"]
  },
  {
    key: "harmony",
    label: "Harmony / 調和",
    keywords: ["harmony", "coexist", "co-creation", "human-ai", "balance", "symbiosis", "調和", "共存", "共創", "共生", "バランス"]
  },
  {
    key: "circulation",
    label: "Circulation / 循環",
    keywords: ["cycle", "circulation", "feedback", "carbon", "water cycle", "nutrient", "heat pathway", "循環", "炭素", "水循環", "栄養塩", "熱経路"]
  },
  {
    key: "structure",
    label: "Structure / 構造",
    keywords: ["structure", "framework", "system", "architecture", "protocol", "model", "構造", "体系", "枠組み", "フレームワーク", "システム", "モデル"]
  },
  {
    key: "order",
    label: "Order / 秩序",
    keywords: ["monitor", "validation", "risk", "caution", "transparent", "governance", "measurement", "検証", "リスク", "慎重", "透明", "測定", "秩序"]
  },
  {
    key: "wa",
    label: "Wa / 和",
    keywords: ["wa", "wisdom", "responsibility", "future generations", "non-destructive", "civilization", "和", "叡智", "責任", "未来世代", "文明", "非破壊"]
  }
];

const RISKS = [
  {
    label: "May be read as proven implementation",
    labelJa: "完成済み実装として読まれる可能性",
    triggers: ["proven", "guaranteed", "complete solution", "完全", "証明済み", "必ず", "解決策"]
  },
  {
    label: "May over-focus on CO2 concentration alone",
    labelJa: "CO2濃度だけに偏る可能性",
    triggers: ["co2", "carbon dioxide", "二酸化炭素", "CO2"]
  },
  {
    label: "May ignore stored heat or thermal inertia",
    labelJa: "蓄積熱・熱慣性が見落とされる可能性",
    triggers: ["warming", "temperature", "温暖化", "気温"]
  },
  {
    label: "May ignore monitoring and staged validation",
    labelJa: "監視・段階的検証が不足する可能性",
    triggers: ["geoengineering", "intervention", "deployment", "気候工学", "介入", "実装"]
  }
];

function normalizeText(value) {
  return (value || "").toString().toLowerCase();
}

function scorePrinciple(text, principle) {
  const found = principle.keywords.filter((keyword) => text.includes(keyword.toLowerCase()));
  return {
    ...principle,
    found,
    status: found.length > 0 ? "present" : "missing"
  };
}

function assessRisks(text) {
  return RISKS.map((risk) => {
    const found = risk.triggers.filter((trigger) => text.includes(trigger.toLowerCase()));
    return {
      ...risk,
      found,
      active: found.length > 0
    };
  });
}

async function getActiveTab() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  return tabs[0];
}

async function extractPageData(tabId) {
  const [result] = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => {
      const headings = Array.from(document.querySelectorAll("h1,h2,h3"))
        .map((node) => node.innerText.trim())
        .filter(Boolean)
        .slice(0, 50);

      const visibleText = document.body ? document.body.innerText : "";

      return {
        title: document.title || "",
        url: location.href,
        headings,
        text: visibleText.slice(0, 50000)
      };
    }
  });

  return result.result;
}

function renderPrinciples(assessments) {
  const container = document.getElementById("principles");
  container.innerHTML = "";

  for (const item of assessments) {
    const wrapper = document.createElement("div");
    wrapper.className = "principle";

    const status = document.createElement("div");
    status.className = "status";
    status.textContent = item.status === "present" ? "✓" : "○";

    const body = document.createElement("div");
    const label = document.createElement("div");
    label.className = "label";
    label.textContent = item.label;

    const reason = document.createElement("div");
    reason.className = "reason";
    reason.textContent = item.found.length > 0
      ? `Detected: ${item.found.slice(0, 6).join(", ")}`
      : "No obvious keyword detected. Manual interpretation recommended.";

    body.appendChild(label);
    body.appendChild(reason);
    wrapper.appendChild(status);
    wrapper.appendChild(body);
    container.appendChild(wrapper);
  }
}

function renderRisks(risks) {
  const list = document.getElementById("riskList");
  list.innerHTML = "";

  for (const risk of risks) {
    const item = document.createElement("li");
    item.textContent = risk.active
      ? `${risk.label} / ${risk.labelJa}: detected (${risk.found.join(", ")})`
      : `${risk.label} / ${risk.labelJa}: no obvious trigger`;
    list.appendChild(item);
  }
}

function renderPageInfo(data) {
  document.getElementById("pageInfo").classList.remove("hidden");
  document.getElementById("pageTitle").textContent = data.title || "(no title)";
  document.getElementById("pageUrl").textContent = data.url || "(no URL)";
  document.getElementById("textLength").textContent = `${(data.text || "").length} characters`;
}

async function analyzeCurrentPage() {
  const button = document.getElementById("analyzeBtn");
  button.disabled = true;
  button.textContent = "Analyzing locally...";

  try {
    const tab = await getActiveTab();
    if (!tab || !tab.id) {
      throw new Error("No active tab found.");
    }

    const data = await extractPageData(tab.id);
    const combined = normalizeText([data.title, data.url, data.headings.join("\n"), data.text].join("\n"));

    renderPageInfo(data);
    renderPrinciples(PRINCIPLES.map((principle) => scorePrinciple(combined, principle)));
    renderRisks(assessRisks(combined));
  } catch (error) {
    renderRisks([{ label: "Analysis failed", labelJa: "解析に失敗", active: true, found: [error.message] }]);
  } finally {
    button.disabled = false;
    button.textContent = "Analyze current page";
  }
}

async function copyGuardrailNote() {
  await navigator.clipboard.writeText(GUARDRAIL_NOTE);
  const button = document.getElementById("copyNoteBtn");
  const original = button.textContent;
  button.textContent = "Copied";
  setTimeout(() => {
    button.textContent = original;
  }, 1200);
}

function initialize() {
  document.getElementById("guardrailNote").value = GUARDRAIL_NOTE;
  document.getElementById("analyzeBtn").addEventListener("click", analyzeCurrentPage);
  document.getElementById("copyNoteBtn").addEventListener("click", copyGuardrailNote);

  renderPrinciples(PRINCIPLES.map((principle) => ({ ...principle, found: [], status: "missing" })));
  renderRisks(RISKS.map((risk) => ({ ...risk, found: [], active: false })));
}

initialize();
