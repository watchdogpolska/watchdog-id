<template>
    <table class="table">
        <thead>
        <th>createdAt</th>
        <th>createdBy</th>
        <th>finishedAt</th>
        <th>status</th>
        </thead>
        <tbody>
        <tr v-for="item in items">
            <td>{{item.createdAt}}</td>
            <td>{{item.createdBy}}</td>
            <td>{{item.finishedAt}}</td>
            <td>{{item.status}}</td>
        </tr>
        </tbody>
    </table>
</template>
<script>
    export default {
        name: 'AccessRequestEventList',
        props: {
            items: {}
        }
    }
</script>
