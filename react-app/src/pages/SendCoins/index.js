import React, { Component } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

class SendCoins extends Component {
  state = {
    address: '',
    amount: 0
  }

  send_coins = (event) => {
    let body = {address: this.state.address, amount: this.state.amount};
    fetch('/sendTransaction', {
      method: "POST", 
      body: JSON.stringify(body), 
      headers: {
        "Content-Type": "application/json",
      }
    }).then((res) => res.json()).then((data) => {
      // TODO: update mempool
      event.preventDefault();
      event.target.reset();
    });
  }

  render() {
    return(
      <div>
        <h1>Send Coins</h1>
        <Form onSubmit={this.send_coins}>
          <Form.Group>
            <Form.Label>Receiver address</Form.Label>
            <Form.Control onChange={(e) => this.setState({address: e.target.value})}></Form.Control>
          </Form.Group>
          <Form.Group>
            <Form.Label>Amount</Form.Label>
            <Form.Control type="number" onChange={(e) => this.setState({amount: e.target.value})}></Form.Control>
          </Form.Group>
          <Button type="submit">
            SEND
          </Button>
        </Form>
      </div>
    )
  }

}

export default SendCoins;