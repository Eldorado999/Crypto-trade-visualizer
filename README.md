# Crypto-trade-visualizer
This is telegram bot for visualization trade history on crypto changes

Send message to bot in this format:
  1. Starts from keywords - "visualize_trade SPOT" or "visualize_trade FUTURES" on which you need
  2. Text in json-like format:
    2.1. "symbol":"DYDXUSDT" any crypto trading pair you need (that exists on Binance)
    2.2. "orders": then list all your orders
      2.2.1. side":"SELL" or "BUY","price":4.78000000,"time":1646864680841 in epoch format.

Example:
visualize_trade FUTURES
{"symbol":"DYDXUSDT","orders":[{"side":"SELL","price":4.78000000,"time":1646864680841},{"side":"BUY","price":4.89000000,"time":1650521511493},{"side":"BUY","price":4.91800000,"time":1650526507597},{"side":"BUY","price":4.93200000,"time":1650526704096},{"side":"SELL","price":3.04700000,"time":1652137890792},{"side":"SELL","price":3.04000000,"time":1652137899425},{"side":"SELL","price":3.02000000,"time":1652137976082},{"side":"BUY","price":2.00200000,"time":1652602379560},{"side":"BUY","price":2.01000000,"time":1652602401149},{"side":"SELL","price":2.06700000,"time":1652620639916},{"side":"SELL","price":2.06400000,"time":1652620649398},{"side":"SELL","price":2.06300000,"time":1652620662631},{"side":"SELL","price":2.05500000,"time":1652621526093},{"side":"SELL","price":2.05200000,"time":1652621533065},{"side":"SELL","price":2.02000000,"time":1652623547755},{"side":"SELL","price":1.75800000,"time":1654113370430}]}

Bot will choose scale for your trades and draw graph with arrows and price on it.
