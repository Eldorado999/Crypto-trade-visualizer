# Crypto-trade-visualizer
This is telegram bot for visualization trade history on crypto changes

Send message to bot in this format:
  1. Starts from keywords - "visualize_trade SPOT" or "visualize_trade FUTURES" on which you need
  2. Text in json-like format:
    2.1. "symbol":"DYDXUSDT" any crypto trading pair you need (that exists on Binance)
    2.2. "orders": then list all your orders
      2.2.1. side":"SELL" or "BUY","price":4.78000000,"time":1646864680841 in epoch format.

Example:
visualize_trade SPOT
{"symbol":"BTCUSDT","orders":[{"side":"BUY","price":19966.30000000,"time":1662454072609},{"side":"BUY","price":18934.36000000,"time":1662563220506},{"side":"BUY","price":19379.00000000,"time":1662682912557},{"side":"SELL","price":20988.44000000,"time":1662729268459},{"side":"BUY","price":21059.18000000,"time":1662729400282},{"side":"BUY","price":22460.00000000,"time":1662992387915},{"side":"SELL","price":19330.00000000,"time":1663661260940},{"side":"BUY","price":19333.00000000,"time":1664436125492},{"side":"SELL","price":19224.10000000,"time":1664458625301},{"side":"SELL","price":19000.00000000,"time":1665591122149},{"side":"SELL","price":19193.20000000,"time":1666446610740},{"side":"SELL","price":19220.83000000,"time":1666448783697},{"side":"SELL","price":19223.24000000,"time":1666448915295},{"side":"SELL","price":20712.51000000,"time":1667825173943},{"side":"SELL","price":19396.47000000,"time":1667825691222}]}

Bot will choose scale for your trades and draw graph with arrows and price on it.

![image](https://user-images.githubusercontent.com/116136718/218323416-67465f42-b374-42c2-badf-7b2af2f710d4.png)


31.01.2023 Added "draw" feature:

  Send message to bot in format: draw {trading pair} {SPOT/FUTURES} {interval} {epoch time first candle}
  
  Don't change the words order and use only spaces as a separator
  
  Example: draw ETHUSDT SPOT 1h 1671912059000
  ![image](https://user-images.githubusercontent.com/116136718/215873151-a190e6b9-aa72-426a-9a43-9ee231d4296a.png)
  
