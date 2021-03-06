'use strict'
import React from 'react'
import {
  Form, Icon, Input, Button, Checkbox,
} from 'antd';
import {registered} from '../../api/user'
import './login.css'

class NormalLoginForm extends React.Component {
  handleSubmit = (e) => {
    console.log('this.props', this.props)
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values);
        registered(values).then((res) => {
          this.props.history.push('/login')
        })
      }
    });
  }

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
        <Form onSubmit={this.handleSubmit} className="login-form">
          <Form.Item>
            {getFieldDecorator('username', {
              rules: [{ required: true, message: 'Please input your username!' }],
            })(
                <Input prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Username" />
            )}
          </Form.Item>
          <Form.Item>
            {getFieldDecorator('password', {
              rules: [{ required: true, message: 'Please input your Password!' }],
            })(
                <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Password" />
            )}
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" className="login-form-button">
              Registered
            </Button>
            <div>
              <a href="#/login">login now!</a>
            </div>
          </Form.Item>
        </Form>
    );
  }
}

const Login = Form.create()(NormalLoginForm);

export default Login