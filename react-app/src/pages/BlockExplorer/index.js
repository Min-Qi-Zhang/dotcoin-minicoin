import React, { Component } from "react";
import Table from 'react-bootstrap/Table';

import './index.css';
import BlockDetail from "../BlockDetail";

class BlockExplorer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      blockchain: [],
      block_detail_hash: '',
      current_index: 0
    };
  };

  get_blockchain = () => {
    fetch('/blocks', {method: "GET"}
    ).then((res) => res.json()).then((data) => {
      let blockchain = data.map((e) => JSON.parse(e))
      this.setState({ blockchain, block_detail_hash: blockchain[this.state.current_index].hash });
    });
  };

  update_block_detail = (hash, index) => {
    this.setState({ block_detail_hash: hash, current_index: index });
  }

  update_block_status = (status) => {
    this.props.update_block_status(status);
  };

  componentDidMount = () => {
    this.get_blockchain();
    this.interval = setInterval(() => {
      this.get_blockchain();
    }, 10000);
  };

  componentWillUnmount = () => {
    clearInterval(this.interval);
  };

  componentDidUpdate = (prevProps) => {
    if (prevProps.need_update !== this.props.need_update && this.props.need_update) {
      this.get_blockchain();
      this.update_block_status(false);
    }
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
                <tr className="table_row" onClick={() => {this.update_block_detail(block.hash, block.index)}}>
                  <td>{block.index}</td>
                  <td>{block.data.length}</td>
                  <td>{new Date(block.timestamp * 1000).toISOString()}</td>
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