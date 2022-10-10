import { Component } from "react";

import './App.css';
import Wallet from "./pages/Wallet";
import BlockExplorer from "./pages/BlockExplorer";
import SendCoins from "./pages/SendCoins";
import TransactionPool from "./pages/TransactionPool";
import JoinNetwork from "./pages/JoinNetwork";

class App extends Component {
  render() {
    return (
      <div className="App">
        <JoinNetwork />
        <Wallet />
        {localStorage.getItem('address') && <SendCoins />}
        <TransactionPool />
        <BlockExplorer />
      </div>
    );
  }
}

export default App;
