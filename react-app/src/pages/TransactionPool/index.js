import React, { Component } from "react";

import TransactionCard from "../../components/TransactionCard";

class TransactionPool extends Component {
  state = {
    transactions: []
  }

  get_transaction_pool = () => {
    fetch('/transactionPool', {method: "GET"})
      .then((res) => res.json()).then((data) => {
        let transactions = data.map((tx) => JSON.parse(tx));
        this.setState({transactions});
    })
  };

  componentDidMount = () => {
    this.get_transaction_pool();
  }

  render() {
    return(
      <div>
        <h1>Transaction Pool</h1>
        {this.state.transactions.map((tx) => {
          return (
            <TransactionCard tx={tx} />
          );
        })}
        {this.state.transactions.length === 0 && <p>No transaction in transaction pool</p>}
      </div>
    )
  }

}

export default TransactionPool;