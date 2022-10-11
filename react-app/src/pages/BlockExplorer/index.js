import React, { Component } from "react";
import Table from 'react-bootstrap/Table';

import './index.css';
import BlockDetail from "../BlockDetail";

class BlockExplorer extends Component {
  state = {
    blockchain: [],
    block_detail_hash: ''
  };

  get_blockchain = () => {
    fetch('/blocks', {method: "GET"}
    ).then((res) => res.json()).then((data) => {
      let blockchain = data.map((e) => JSON.parse(e))
      this.setState({ blockchain, block_detail_hash: blockchain[0].hash });
    });
  };

  update_block_detail = (hash) => {
    this.setState({ block_detail_hash: hash });
  }

  componentDidMount = () => {
    this.get_blockchain();
  };

  render() {
    return(
      <div>
        <h1>Block Explorer</h1>
        <Table striped bordered hover variant="dark">
          <thead>
            <tr>
              <th>Index</th>
              <th>Transactions</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {this.state.blockchain.map((block) => {
              return (
                <tr className="table_row" onClick={() => {this.update_block_detail(block.hash)}}>
                  <td>{block.index}</td>
                  <td>{block.data.length}</td>
                  <td>{new Date(block.timestamp * 1000).toDateString()}</td>
                </tr>
              );
            })};
          </tbody>
        </Table>
        {this.state.block_detail_hash && <BlockDetail hash={this.state.block_detail_hash} />}
      </div>
    )
  };

}

export default BlockExplorer;