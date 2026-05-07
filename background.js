chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      // 1. Try to find the main H1 (often better than document.title)
      const h1 = document.querySelector('h1');
      const articleTitle = h1 ? h1.innerText.trim() : document.title;

      // 2. Extract only article paragraphs (for cleaner reading)
      // Instead of innerText, select only p, h1, h2 etc.
      const contentElements = document.querySelectorAll('article p, main p, p');
      const body = Array.from(contentElements)
        .map(p => p.innerText.trim())
        .filter(text => text.length > 30) // Ignore crumbs like "Share on FB"
        .join('\n\n');

      return { title: articleTitle, body: body };
    }
  }).then(results => {
    const data = results[0].result;
    
    fetch('https://jindracerny.pythonanywhere.com/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(async response => {
      const result = await response.json();
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (msg) => { alert(msg); },
        args: [result.status === "success" ? "Odesláno: " + result.title : "Chyba: " + result.error]
      });
    });
  });
});