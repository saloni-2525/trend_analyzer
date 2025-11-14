const API_BASE = "http://127.0.0.1:8000";

document.getElementById("searchBtn").addEventListener("click", async () => {
  const keyword = document.getElementById("keyword").value.trim();
  if (!keyword) return alert("Please enter a keyword!");

  document.getElementById("summary-section").classList.add("hidden");
  document.getElementById("charts").classList.add("hidden");
  document.getElementById("overall-summary").innerText = "Analyzing...";

  try {
    // 1️⃣ Fetch trend data
    const trendRes = await fetch(`${API_BASE}/trend/${keyword}`);
    const trendData = await trendRes.json();

    // 2️⃣ Fetch summary
    const summaryRes = await fetch(`${API_BASE}/trend_summary/${keyword}`);
    const summaryData = await summaryRes.json();
    console.log("Summary Data:", summaryData);

    document.getElementById("overall-summary").innerText =
      summaryData.overall_summary ||
      summaryData.summary ||
      summaryData.data?.summary ||
      "⚠️ No summary available.";

    document.getElementById("summary-section").classList.remove("hidden");

    // 3️⃣ Charts
    renderCharts(trendData.results);
    document.getElementById("charts").classList.remove("hidden");
  } catch (err) {
    console.error("Error fetching summary:", err);
    document.getElementById("overall-summary").innerText =
      "⚠️ Failed to fetch summary. Check console for details.";
    document.getElementById("summary-section").classList.remove("hidden");
  }
});


function renderCharts(results) {
  const sentimentTotals = { pos: 0, neu: 0, neg: 0 };
  const bySource = {
    reddit: { pos: 0, neu: 0, neg: 0 },
    twitter: { pos: 0, neu: 0, neg: 0 },
    news: { pos: 0, neu: 0, neg: 0 },
  };

  results.forEach((r) => {
    sentimentTotals.pos += r.sentiment.pos;
    sentimentTotals.neu += r.sentiment.neu;
    sentimentTotals.neg += r.sentiment.neg;

    if (bySource[r.source]) {
      bySource[r.source].pos += r.sentiment.pos;
      bySource[r.source].neu += r.sentiment.neu;
      bySource[r.source].neg += r.sentiment.neg;
    }
  });

  // PIE CHART — Overall Sentiment
  const pieCtx = document.getElementById("pieChart").getContext("2d");
  new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [
        {
          data: [sentimentTotals.pos, sentimentTotals.neu, sentimentTotals.neg],
          backgroundColor: ["#4CAF50", "#FFC107", "#F44336"],
        },
      ],
    },
    options: { responsive: true, plugins: { legend: { position: "bottom" } } },
  });

  // BAR CHART — Sentiment by Source
  const barCtx = document.getElementById("sentimentChart").getContext("2d");
  new Chart(barCtx, {
    type: "bar",
    data: {
      labels: ["Reddit", "Twitter", "News"],
      datasets: [
        {
          label: "Positive",
          data: [bySource.reddit.pos, bySource.twitter.pos, bySource.news.pos],
          backgroundColor: "#4CAF50",
        },
        {
          label: "Neutral",
          data: [bySource.reddit.neu, bySource.twitter.neu, bySource.news.neu],
          backgroundColor: "#FFC107",
        },
        {
          label: "Negative",
          data: [bySource.reddit.neg, bySource.twitter.neg, bySource.news.neg],
          backgroundColor: "#F44336",
        },
      ],
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { position: "bottom" } },
    },
  });
}

// ...inside your renderCharts or main chart section...

// Radar Chart
// const radarCanvas = document.getElementById("radarChart");
// if (radarCanvas) {
//   const radarCtx = radarCanvas.getContext("2d");
//   new Chart(radarCtx, {
//     type: "radar",
//     data: {
//       labels: ["Positive", "Neutral", "Negative"],
//       datasets: [
//         {
//           label: "Reddit",
//           data: [bySource.reddit.pos, bySource.reddit.neu, bySource.reddit.neg],
//           fill: true,
//           backgroundColor: "rgba(54, 162, 235, 0.2)",
//           borderColor: "rgba(54, 162, 235, 1)",
//         },
//         {
//           label: "Twitter",
//           data: [
//             bySource.twitter.pos,
//             bySource.twitter.neu,
//             bySource.twitter.neg,
//           ],
//           fill: true,
//           backgroundColor: "rgba(255, 206, 86, 0.2)",
//           borderColor: "rgba(255, 206, 86, 1)",
//         },
//         {
//           label: "News",
//           data: [bySource.news.pos, bySource.news.neu, bySource.news.neg],
//           fill: true,
//           backgroundColor: "rgba(75, 192, 192, 0.2)",
//           borderColor: "rgba(75, 192, 192, 1)",
//         },
//       ],
//     },
//     options: {
//       responsive: true,
//       scales: { r: { angleLines: { color: "#ddd" }, suggestedMin: 0 } },
//     },
//   });
// }

// // Horizontal Bar: Total Mentions
// const sourceTotalMentions = [
//   results.filter((r) => r.source === "reddit").length,
//   results.filter((r) => r.source === "twitter").length,
//   results.filter((r) => r.source === "news").length,
// ];
// const hbarCanvas = document.getElementById("sourceBarChart");
// if (hbarCanvas) {
//   const hbarCtx = hbarCanvas.getContext("2d");
//   new Chart(hbarCtx, {
//     type: "bar",
//     data: {
//       labels: ["Reddit", "Twitter", "News"],
//       datasets: [
//         {
//           label: "Total Mentions",
//           data: sourceTotalMentions,
//           backgroundColor: ["#36A2EB", "#FFCE56", "#4BC0C0"],
//         },
//       ],
//     },
//     options: {
//       indexAxis: "y",
//       responsive: true,
//       plugins: { legend: { display: false } },
//     },
//   });
// }
