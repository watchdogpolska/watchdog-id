import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import {AUTH_REQUEST, LOGOUT_REQUEST, AUTH_SUCCESS, LOGOUT_SUCCESS, AUTH_ERROR, LOGOUT_ERROR} from '@/mutation-types';
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    access_request: require('./access_request').default,
    service: require('./service').default
  },
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
    session_id: localStorage.getItem('session_id') || '',
    user_id: localStorage.getItem('user_id') || '',
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
  },
  mutations: {
    [AUTH_REQUEST] (state) {
      state.status = 'loading'
    },
    [LOGOUT_REQUEST] (state) {
      state.status = 'loading'
    },
    [AUTH_SUCCESS] (state, payload) {
      state.status = 'success';
      state.token = payload.token;
      state.username = payload.username;
      state.user_id = payload.user_id;
      state.session_id = payload.session_id;
    },
    [LOGOUT_SUCCESS] (state) {
      state.status = 'success';
      state.token = '';
      state.username = '';
      state.session_id = '';
    },
    [AUTH_ERROR] (state) {
      state.status = 'error'
    },
    [LOGOUT_ERROR] (state) {
      state.status = 'error'
    },
  },
  actions: {
    async login({commit}, data) {

      commit(AUTH_REQUEST);
      try {
        const resp = await axios.post('/v1/user/me/session', data);
        const token = resp.data.secret;
        const session_id=  resp.data._id;
        const user_id = resp.data.user;
        localStorage.setItem('token', token);
        localStorage.setItem('session_id', session_id);
        localStorage.setItem('user_id', user_id);
        axios.defaults.headers.common['x-auth-token'] = token;
        const user_resp = await axios({
          url: `/v1/user/${user_id}`
        });
        const username = user_resp.data.username;
        localStorage.setItem('username', username);
        commit(AUTH_SUCCESS, {
          token,
          username,
          session_id,
          user_id,
        });
        return resp;
      } catch (err) {
        console.log(AUTH_ERROR, err);
        commit(AUTH_ERROR);
        localStorage.removeItem('token');
        throw err;
      }
    },
    async logout({commit, state}, data) {
      commit(LOGOUT_REQUEST);
      try {
        const resp = await axios.delete(`/v1/user/${state.user_id}/session/${state.session_id}`);
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('session_id');
        localStorage.removeItem('user_id');
        commit(LOGOUT_SUCCESS);
        return resp;
      } catch (err) {
        console.log(LOGOUT_ERROR, err);
        commit(LOGOUT_ERROR);
        throw err;
      }
    },
  },
});
