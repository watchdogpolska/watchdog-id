import axios from 'axios';
import {
  ADD_ITEM_ERROR,
  ADD_ITEM_REQUEST,
  ADD_ITEM_SUCCESS
} from '@/mutation-types';

export default {
  namespaced: true,
  state: {
    status: '',
    items: [],
    item: {},
    pagination: {
      page: 1,
      limit: 12,
      total: 0
    }
  },
  getters: {
    getModel: state => state.item,
    getItems: state => state.items,
  },
  mutations: {
    [ADD_ITEM_REQUEST](state) {
      state.status = 'loading'
    },
    [ADD_ITEM_SUCCESS](state, payload) {
      state.status = 'success';
      state.items.unshift(payload)
    },
    [ADD_ITEM_ERROR](state) {
      state.status = 'error';
    },
  },
  actions: {
    async addItem({commit}, data) {
      commit(ADD_ITEM_REQUEST);
      try {
        const resp = await axios.post('/v1/service/', data);
        commit(ADD_ITEM_SUCCESS, resp.data);
        return resp;
      } catch (err) {
        commit(ADD_ITEM_ERROR);
        throw err;
      }
    },
  }
};
