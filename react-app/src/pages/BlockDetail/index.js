import React, { Component } from "react";
import Table from 'react-bootstrap/Table';
import TransactionCard from "../../components/TransactionCard";

class BlockDetail extends Component {
  constructor(props) {
    super(props);
    this.state = {
      block: null
    };
  };

  get_block = () => {
    fetch(`/block/${this.props.hash}`, {method: "GET"}
    ).then((res) => res.json()).then((data) => {
      this.setState({ block: data });
    }).catch((err) => {
      console.log(err);
    });
  };

  componentDidMount = () => {
    this.get_block();
  };

  componentDidUpdate = (prevProps) => {
    if (prevProps.hash !== this.props.hash) {
      this.get_block();
    }
  };

  render() {
    return(
      <div>
        {this.state.block &&
        <div>
          <h1>Block #{this.state.block.index}</h1>
          <Table>
            <tbody>
              <tr>
                <td>Hash</td>
                <td>{this.state.block.hash}</td>
              </tr>
              <tr>
                <td>Previous hash</td>
                <td>{this.state.block.prev_hash}</td>
              </tr>
              <tr>
                <td>Timestamp</td>
                <td>{new Date(this.state.block.timestamp * 1000).toISOString()}</td>
              </tr>
              <tr>
                <td>Difficulty</td>
                <td>{this.state.block.difficulty}</td>
              </tr>
              <tr>
                <td>Nonce</td>
                <td>{this.state.block.nonce}</td>
              </tr>
              <tr>
                <td>Number of transactions</td>
                <td>{this.state.block.data.length}</td>
              </tr>
            </tbody>
          </Table>

          <h3>Transactions</h3>
          {this.state.block.data.map((tx) => {
            return (
              <TransactionCard tx={tx} />
            );
          })}
        </div>
        }
      </div>
    )
  }

}

export default BlockDetail;