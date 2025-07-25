#include<iostream>
#include<vector>
#include<queue>
#include<utility>
#include<climits>
using namespace std;

vector<int> dijkstra(vector<vector<pair<int,int>>>&adj,int src,int V)
{
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
    vector<int>dist(V,INT_MAX);
    dist[src] = 0;
    pq.push({0,src});
    while(!pq.empty()){
        int dis = pq.top().first;
        int node = pq.top().second;
        pq.pop();
        for(auto i : adj[node]){
            int wt = i.second;
            int adjNode = i.first;
            if(dis + wt < dist[adjNode]){
                dist[adjNode] = dis + wt;
                pq.push({dist[adjNode],adjNode});
            }
        }
    }
    return dist;
}

int main()
{
    int V,E,src;
    cout<<"Enter the vertices and edges";
    cin>>V>>E;
    cout<<"Enter the source";
    cin>>src;
    vector<vector<pair<int,int>>>adj(V);
    for(int i = 0;i<E;i++)
    {
        int a,b,c;
        cin>>a>>b>>c;
        adj[a].push_back({b,c});
        adj[b].push_back({a,c});
    }
    vector<int> distance = dijkstra(adj,src,V);
    for (int i = 0; i < V; ++i){
        cout << "Distance from " << src << " to " << i << " is " << distance[i] << endl;
    }
    return 0;
}