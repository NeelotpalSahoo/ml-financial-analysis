const socket = io('http://127.0.0.1:5000');

function fetchCompany() {
  const company = document.getElementById('companySelector').value;
  fetch(`/start?company=${company}`);
}

socket.on('analysis_update', (data) => {
  document.getElementById('output').innerHTML += `
    <div>
      <h4>${data.company}</h4>
      <p>Pros: ${data.pros.join(', ')}</p>
      <p>Cons: ${data.cons.join(', ')}</p>
    </div>
    <hr/>
  `;
});
