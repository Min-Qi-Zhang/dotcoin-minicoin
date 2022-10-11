import React, { Component } from "react";
import Card from 'react-bootstrap/Card';

import './index.css';
import UTXOCard from "../UTXOCard";

class TransactionCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: '',
      tx_ins: [],
      tx_outs: []
    };
  };

  componentDidMount = () => {
    this.setState({ id: this.props.tx.id, tx_ins: this.props.tx.tx_ins, tx_outs: this.props.tx.tx_outs });
  };

  componentDidUpdate = (prevProps) => {
    if (prevProps.tx.id !== this.props.tx.id) {
      this.setState({ id: this.props.tx.id, tx_ins: this.props.tx.tx_ins, tx_outs: this.props.tx.tx_outs });
    }
  }

  render() {
    return(
      <Card className="transaction_card">
        <Card.Body>
          <Card.Title>{this.state.id}</Card.Title>
          <div className="flex_row">
            <div className="tx_ins_box">
              {this.state.tx_ins.map((tx_in) => {
                return (
                  <UTXOCard tx_in={tx_in} />
                );
              })}
            </div>
            <div className="arrow_box">{ '->' }</div>
            <div className="tx_outs_box">
              {this.state.tx_outs.map((tx_out) => {
                return (
                  <UTXOCard tx_out={tx_out} />
                )
              })}
            </div>
          </div>
        </Card.Body>
      </Card>
    )
  };

}

export default TransactionCard;