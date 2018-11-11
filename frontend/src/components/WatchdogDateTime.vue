<template>
  <time :datetime="time" :title="time">{{time | relativeTime}} XX</time>
</template>
<script>
  // const moment = require('momentjs'); // TODO: Unify that!
  import moment from 'moment';
  export default {
    name: 'watchdog-time',
    props: {
      time: null,
    },
    filters: {
      relativeTime: function (value) {
        if (!value) return '';
        return moment(value).calendar()
      },

    }
  };
</script>
