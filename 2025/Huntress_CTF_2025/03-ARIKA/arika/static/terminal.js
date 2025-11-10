(() => {
  const screen = document.getElementById("screen");

  function appendLine(text, cls) {
    const pre = document.createElement("pre");
    pre.className = "line" + (cls ? " " + cls : "");
    pre.textContent = text;
    screen.appendChild(pre);
    scrollToBottom();
    return pre;
  }
  
  function createPromptLine() {
    const pre = document.createElement("pre");
    pre.className = "line prompt-line";
    const promptSpan = document.createElement("span");
    promptSpan.className = "prompt-text";
    promptSpan.textContent = window.PROMPT;
    const editSpan = document.createElement("span");
    editSpan.className = "prompt-editable";
    editSpan.contentEditable = "true";
    editSpan.spellcheck = false;
    editSpan.setAttribute("aria-label", "Terminal input");
    editSpan.setAttribute("role", "textbox");
    editSpan.tabIndex = 0;
    pre.appendChild(promptSpan);
    pre.appendChild(editSpan);
    screen.appendChild(pre);
    scrollToBottom();
    
    placeCaretAtEnd(editSpan);
    
    editSpan.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const raw = editSpan.textContent || "";
        const line = raw.replace(/\r?\n/g, ""); 
        
        pre.textContent = window.PROMPT + line;
        
        runCommand(line);
      } else if (e.key === "Tab") {
        
        e.preventDefault();
        insertAtCaret(editSpan, "  ");
      }
    });
    
    screen.addEventListener("click", (ev) => {
      
      const curEdit = document.querySelector(".prompt-editable");
      if (curEdit) {
        placeCaretAtEnd(curEdit);
        curEdit.focus();
      }
    });
    return editSpan;
  }
  
  function appendBlocks(stdout, stderr) {
    
    appendLine("");
    if (stdout) stdout.split(/\r?\n/).forEach((l, i, a) => {
      if (i === a.length - 1 && l === "") return; 
      appendLine(l);
    });
    if (stderr) stderr.split(/\r?\n/).forEach((l, i, a) => {
      if (i === a.length - 1 && l === "") return;
      appendLine(l);
    });
  }
  
  function scrollToBottom() {
    screen.scrollTop = screen.scrollHeight;
  }
  
  function placeCaretAtEnd(el) {
    el.focus();
    if (typeof window.getSelection !== "undefined"
        && typeof document.createRange !== "undefined") {
      const range = document.createRange();
      range.selectNodeContents(el);
      range.collapse(false);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    }
  }
  
  function insertAtCaret(el, text) {
    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);
    range.deleteContents();
    const node = document.createTextNode(text);
    range.insertNode(node);
    
    range.setStartAfter(node);
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);
    
    placeCaretAtEnd(el);
  }
  
  function runCommand(line) {
    if (line.trim() === "") {
      
      appendLine("");
      createPromptLine(); 
      return;
    }
    
    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: line })
    })
      .then(r => r.json())
      .then(({ ok, stdout, stderr, code, clear }) => {
        if (clear) {
          screen.innerHTML = "";
          createPromptLine();
          return;
        }
        appendBlocks(stdout || "", stderr || "");
        if (!ok && code !== 0 && !(stderr && stderr.length)) {
          appendLine(`(exit ${code})`);
        }
        
        createPromptLine();
      })
      .catch(err => {
        appendLine("");
        appendLine(`Client error: ${err}`);
        createPromptLine();
      });
  }
  
  window.addEventListener("load", () => {
    createPromptLine();
  });
})();
