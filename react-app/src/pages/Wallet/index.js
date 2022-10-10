import React, { Component } from "react";
import Button from 'react-bootstrap/Button';

class Wallet extends Component {
  state = {
    address: "You don't have an address yet, please generate one.",
    balance: 0
  }

  get_balance = () => {
    fetch('/balance', {method: "GET"}
    ).then((res) => res.json()).then((data) => {
      this.setState({ balance: data.balance });
    });
  };

  get_address = () => {
    fetch('/address', {method: "GET"}
    ).then((res) => res.json()).then((data) => {
      this.setState({ address: data.address });
      localStorage.setItem('address', data.address)
    });
  };

  init_wallet = () => {
    fetch('/getKeyPair', {methd: "GET"}
    ).then((res) => res.json()).then((data) => {
      this.setState({ address: data.address });
      localStorage.setItem('address', data.address)
    })
  }

  componentDidMount = () => {
    const address = localStorage.getItem('address')
    if (address) {
      this.setState({ address })
    } else {
      this.get_address();
    }

    this.get_balance();
  }

  render() {
    return(
      <div>
        <h1>Wallet</h1>
        <p>Your public address: </p>
        <h4>{this.state.address}</h4>
        <Button 
          disabled={localStorage.getItem('address')}
          onClick={this.init_wallet}
        >
          Generate Key Pair
        </Button>

        <p>Your balance: </p>
        <h4>{this.state.balance}</h4>
      </div>
    )
  }

}

export default Wallet;