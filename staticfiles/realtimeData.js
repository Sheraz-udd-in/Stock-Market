
  const API_KEY = 'd1jl5vpr01qvg5gv7rn0d1jl5vpr01qvg5gv7rng';
  const ticker = 'AAPL';
  const socket = new WebSocket(`wss://ws.finnhub.io?token=${API_KEY}`);

  socket.addEventListener('open', function () {
    socket.send(JSON.stringify({ type: 'subscribe', symbol: ticker }));
  });

  socket.addEventListener('message', function (event) {
    const data = JSON.parse(event.data);
    if (data.type === 'trade') {
      const price = data.data[0].p;
      document.getElementById().innerText = price.toFixed(2);
    }
  });


  window.addEventListener('beforeunload', () => {
    socket.send(JSON.stringify({ type: 'unsubscribe', symbol: ticker }));
    socket.close();
  });