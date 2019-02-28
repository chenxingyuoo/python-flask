import React, {Component} from 'react';
import {Table, Modal, message} from 'antd';
import request from '../../../js/utils/request';
import SidebarLayout from '../../layout/sidebarLayout';

const confirm = Modal.confirm;

class UserList extends Component {
  constructor() {
    super()

    this.state = {
      params: {
        currentPage: 1,
        pageSize: 5
      },
      data: {
        list: []
      }
    };
  }

  componentDidMount() {
    this.getList()
  }

  render() {
    const columns = [{
      title: 'Name',
      dataIndex: 'username',
    }, {
      title: 'Password',
      dataIndex: 'password',
    }, {
      title: 'Action',
      dataIndex: 'action',
      render: (text, record, index) => {
        return (
            <span>
              <a onClick={this.deleteUser.bind(this, record, index)}>删除</a>
            </span>
        )
      },
    }];
    return (
        <SidebarLayout>
          <div className="App">
            <Table dataSource={this.state.data.list} columns={columns} pagination={{total: this.state.data.total, onChange: this.pageChange.bind(this)}}/>
          </div>
        </SidebarLayout>
    );
  }

  getList() {
    request.get({
      url: '/api/user/list',
      data: this.state.params
    }).then((data) => {
      this.setState({
        data: data.data
      })
    })
  }

  pageChange(val){
    this.state.params.currentPage = val
    this.setState({
      params: this.state.params
    })
    this.getList()
  }

  deleteUser(record, index) {
    confirm({
      title: 'Do you Want to delete these items?',
      content: '',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk: () => {
        request.post({
          url: '/api/user/delete',
          data: {
            id: record._id
          }
        }).then((data) => {
          message.success('删除成功')
          this.getList()
        })
      },
      onCancel() {
        console.log('Cancel');
      },
    });

  }
}

export default UserList;
