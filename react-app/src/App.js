import { Component } from "react";

import './App.css';
import Wallet from "./pages/Wallet";
import BlockExplorer from "./pages/BlockExplorer";
import SendCoins from "./pages/SendCoins";
import TransactionPool from "./pages/TransactionPool";
import JoinNetwork from "./pages/JoinNetwork";
import UTXOPage from "./pages/UTXOPage";

class App extends Component {
  state = {
    need_update: []
  };

  update_block_status = (need_update) => {
    this.setState({need_update})
  }

  render() {
    return (
      <div className="App">
        <JoinNetwork need_update={this.state.need_update} update_block_status={this.update_block_status} /> <hr />
        <Wallet /> <hr />
        {localStorage.getItem('address') && <><UTXOPage type='MY' /><hr /></>}
        {localStorage.getItem('address') && <><UTXOPage type='ALL' /><hr /></>}
        {localStorage.getItem('address') && <><SendCoins /><hr /></>}
        <TransactionPool /> <hr />
        <BlockExplorer need_update={this.state.need_update} update_block_status={this.update_block_status} /> <hr />
      </div>
    );
  }
}

export default App;
