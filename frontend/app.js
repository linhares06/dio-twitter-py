new Vue({
    el: '#app',
    components: {
        'trend-list': {
            data() {
                return {
                    trends: []
                };
            },
            created() {
                this.fetchTrends();
            },
            methods: {
                async fetchTrends() {
                    const response = await fetch('http://localhost:8000/trends');
                    const data = await response.json();
                    
                    this.trends = data;
                }
            },
            template: `
                <div>
                    <h1>Twitter Trends</h1>
                    <ul>
                        <li v-for="trend in trends" :key="trend.name">
                            <a :href="trend.url" target="_blank">{{ trend.name }}</a>
                        </li>
                    </ul>
                </div>
            `
        }
    }
});