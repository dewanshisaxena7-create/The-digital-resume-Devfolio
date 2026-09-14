"""
Seed Script to populate SQLite database with Devanshi's real GitHub projects,
achievements, and clean C++ DSA solutions.
Run: `python seed_data.py`
"""

from app import app
from models import db, Project, Achievement, DSAProblem

def seed_database():
    with app.app_context():
        # Create database tables
        db.create_all()

        # Reset tables
        db.session.query(Project).delete()
        db.session.query(Achievement).delete()
        db.session.query(DSAProblem).delete()

        print("Seeding Devanshi's Real Projects...")
        
        p1 = Project(
            title="College Connect Platform",
            subtitle="Full-stack portal connecting students, faculty, and academic resources",
            description="Comprehensive college web portal facilitating real-time announcements, peer collaboration, assignment tracking, and resource management with robust Flask backend APIs and SQL database integration.",
            tech_stack="Flask, Python, SQL, HTML5, CSS3, JavaScript",
            github_url="https://github.com/dewanshisaxena7-create/College-connect-",
            live_demo_url="",
            category="Web App",
            featured=True
        )

        p2 = Project(
            title="DAA (Design & Analysis of Algorithms) C++ Repository",
            subtitle="Comprehensive C++ implementations of fundamental & advanced algorithms",
            description="Curated repository of algorithmic solutions including Graph algorithms (BFS, DFS, Dijkstra), Dynamic Programming, Greedy approaches, Sorting benchmarks, and time/space complexity analysis in modern C++.",
            tech_stack="C++, Data Structures, Algorithms, STL",
            github_url="https://github.com/dewanshisaxena7-create/IC-2K23-24--DAA-Devanshi-Saxena-",
            live_demo_url="",
            category="C++ / Systems",
            featured=True
        )

        p3 = Project(
            title="Student Result Analyzer",
            subtitle="Academic performance calculation and marks analytics application",
            description="Data analysis tool designed to process student academic grades, compute GPA metrics, generate performance summaries, and present statistical analysis of examination scores.",
            tech_stack="Python, SQL, Data Analytics, Web Interface",
            github_url="https://github.com/dewanshisaxena7-create/Student-result-analyzer-",
            live_demo_url="",
            category="Web App",
            featured=True
        )

        p4 = Project(
            title="Thread-Safe LRU Cache in C++",
            subtitle="O(1) Get & Put LRU cache using Doubly Linked List and Hash Map with mutex locks",
            description="High-performance Least Recently Used (LRU) Cache data structure implemented in C++ using std::list and std::unordered_map, featuring thread-safe operations guarded with std::mutex.",
            tech_stack="C++, Multithreading, DSA, STL",
            github_url="https://github.com/dewanshisaxena7-create",
            live_demo_url="",
            category="C++ / Systems",
            featured=True
        )

        db.session.add_all([p1, p2, p3, p4])

        print("Seeding Achievements...")
        a1 = Achievement(
            title="Solved 400+ Data Structures & Algorithms Problems",
            category="Competitive Programming",
            issuer="LeetCode & GeeksforGeeks",
            date_achieved="2026",
            description="Consistent problem solver mastering Arrays, Strings, Trees, Graphs, Dynamic Programming, and Recursion using C++.",
            icon="code",
            verification_url="https://github.com/dewanshisaxena7-create"
        )

        a2 = Achievement(
            title="Lead Full-Stack Developer — College Connect",
            category="Academic / Project",
            issuer="College Project Lead",
            date_achieved="2026",
            description="Designed and deployed full-stack web architecture with Flask backend, SQLite database integration, and intuitive frontend UI.",
            icon="trophy",
            verification_url="https://github.com/dewanshisaxena7-create/College-connect-"
        )

        a3 = Achievement(
            title="C++ Object-Oriented Programming & Systems Specialization",
            category="Certification",
            issuer="Software Engineering Certification",
            date_achieved="2025",
            description="Mastered core C++ concepts including object-oriented design, dynamic memory allocation, STL containers, and algorithm design.",
            icon="certificate",
            verification_url=""
        )

        db.session.add_all([a1, a2, a3])

        print("Seeding DSA C++ Solutions...")
        dsa1 = DSAProblem(
            title="LRU Cache Implementation",
            category="Arrays & Hashing",
            difficulty="Medium",
            time_complexity="O(1) Get & Put",
            space_complexity="O(Capacity)",
            problem_statement="Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement get(key) and put(key, value) in O(1) time complexity.",
            cpp_solution="""#include <iostream>
#include <unordered_map>
#include <list>

class LRUCache {
private:
    int capacity;
    std::list<std::pair<int, int>> cacheList;
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> cacheMap;

public:
    LRUCache(int cap) : capacity(cap) {}

    int get(int key) {
        if (cacheMap.find(key) == cacheMap.end()) return -1;
        cacheList.splice(cacheList.begin(), cacheList, cacheMap[key]);
        return cacheMap[key]->second;
    }

    void put(int key, int value) {
        if (cacheMap.find(key) != cacheMap.end()) {
            cacheMap[key]->second = value;
            cacheList.splice(cacheList.begin(), cacheList, cacheMap[key]);
            return;
        }

        if (cacheList.size() == capacity) {
            int lruKey = cacheList.back().first;
            cacheList.pop_back();
            cacheMap.erase(lruKey);
        }

        cacheList.push_front({key, value});
        cacheMap[key] = cacheList.begin();
    }
};""",
            explanation="Uses a doubly-linked list (`std::list`) to keep track of access order and an `unordered_map` mapping keys to list iterators to guarantee O(1) operations for both get and put."
        )

        dsa2 = DSAProblem(
            title="Dijkstra's Shortest Path Algorithm",
            category="Trees & Graphs",
            difficulty="Hard",
            time_complexity="O((V + E) log V)",
            space_complexity="O(V + E)",
            problem_statement="Given a weighted directed graph and a source vertex, find the shortest distance from the source vertex to all other vertices in the graph.",
            cpp_solution="""#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

vector<int> dijkstra(int V, vector<vector<pair<int, int>>>& adj, int src) {
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    vector<int> dist(V, INT_MAX);

    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue;

        for (auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;

            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}""",
            explanation="Utilizes a C++ `std::priority_queue` min-heap to greedily expand the vertex with the smallest tentative distance, relaxing adjacent edges until all shortest paths are computed."
        )

        dsa3 = DSAProblem(
            title="0/1 Knapsack Dynamic Programming",
            category="Dynamic Programming",
            difficulty="Medium",
            time_complexity="O(N * W)",
            space_complexity="O(W) Space Optimized",
            problem_statement="Given weights and values of N items, put these items in a knapsack of capacity W to get the maximum total value in the knapsack.",
            cpp_solution="""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int knapsackDP(int W, const vector<int>& wt, const vector<int>& val, int n) {
    vector<int> dp(W + 1, 0);

    for (int i = 0; i < n; i++) {
        for (int w = W; w >= wt[i]; w--) {
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
        }
    }
    return dp[W];
}""",
            explanation="Uses 1D space optimization by running the inner capacity loop backwards from W down to item weight, preventing double counting while preserving O(W) extra memory."
        )

        db.session.add_all([dsa1, dsa2, dsa3])
        db.session.commit()
        print("Database populated with Devanshi's real GitHub projects!")

if __name__ == '__main__':
    seed_database()
