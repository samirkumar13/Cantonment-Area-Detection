document.addEventListener("DOMContentLoaded", () => {
  const uploadBtn      = document.getElementById("uploadBtn");
  const detectBtn      = document.getElementById("detectBtn");
  const fileInput      = document.getElementById("fileInput");
  const previewImg     = document.getElementById("previewImg");
  const resultImg      = document.getElementById("resultImg");
  const downloadLink   = document.getElementById("downloadLink");
  const processingText = document.getElementById("processingText");
  const detectionList  = document.getElementById("detectionList");
  const totalCountEl   = document.getElementById("totalCount");
  const boxesContainer = document.getElementById("boxesContainer");
  const previewBox     = document.getElementById("previewBox");
  const resultBox      = document.getElementById("resultBox");

  let currentFile = null;

  // Initially hide boxes and detect button
  boxesContainer.style.display = 'none';
  detectBtn.style.display = 'none';

  // Upload handling
  uploadBtn.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (!file) return;
    currentFile = file;
    previewImg.src = URL.createObjectURL(file);
    resultImg.src = "";
    downloadLink.style.display = "none";

    // Show only preview box and detect button
    boxesContainer.style.display = 'flex';
    previewBox.style.display = 'block';
    resultBox.style.display = 'none';
    detectBtn.style.display = 'inline-block';

    // Reset sidebar
    totalCountEl.textContent = "0";
    detectionList.innerHTML = "<li style='opacity:0.7'>Ready to detect...</li>";
  });

  // Detect
  detectBtn.addEventListener("click", async () => {
    if (!currentFile) {
      alert("Please upload an image first");
      return;
    }
    detectBtn.disabled = true;

    // Show processing indicator
    processingText.style.display = "block";
    resultImg.style.display = "none";
    downloadLink.style.display = "none";

    const fd = new FormData();
    fd.append("images[]", currentFile);

    try {
      const res = await fetch("/api/process", { method: "POST", body: fd });
      const data = await res.json();

      if (data.error) {
        alert(data.error);
        processingText.style.display = "none";
      } else {
        // update result image and download link
        processingText.style.display = "none";
        resultImg.src = data.processedImages[0].url;
        resultImg.style.display = "block";
        downloadLink.href = data.processedImages[0].downloadUrl;
        downloadLink.style.display = "inline-block";

        // Show result box (preview remains visible too)
        resultBox.style.display = 'block';

        // Update sidebar
        const detections = data.detections || {};
        const total = data.total || 0;
        const classColors = data.classColors || {};
        totalCountEl.textContent = total;

        const sorted = Object.entries(detections).sort((a, b) => b[1] - a[1]);

        detectionList.innerHTML = "";
        sorted.forEach(([cls, cnt]) => {
          const li = document.createElement("li");

          const colorBox = document.createElement('span');
          colorBox.className = 'color-box';
          colorBox.style.backgroundColor = classColors[cls] || '#dddddd';

          const nameSpan = document.createElement('span');
          nameSpan.textContent = cls;

          const countPill = document.createElement('span');
          countPill.className = 'count-pill';
          countPill.textContent = cnt;

          li.appendChild(colorBox);
          li.appendChild(nameSpan);
          li.appendChild(countPill);

          if (cnt > 0) li.classList.add("detected"); else li.classList.add("zero");
          detectionList.appendChild(li);
        });
      }
    } catch (e) {
      alert("Detection failed");
      console.error(e);
      processingText.style.display = "none";
    } finally {
      detectBtn.disabled = false;
    }
  });
});
