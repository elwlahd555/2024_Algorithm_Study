#include <stdio.h>
#include <limits.h>

#define MAX_N 50

struct Agent {
    int a, b, c;
};

int min(int a, int b) {
    return (a < b) ? a : b;
}

int calculateMinimumDestruction(struct Agent agents[], int n) {
    int minDestruction = INT_MAX;

    for (int i = 0; i < n; ++i) {
        // 선택한 요원의 능력치를 갤럭시와 공유
        int sharedPower = agents[i].a + agents[i].b + agents[i].c;

        // 나머지 요원의 두 능력치를 소멸
        int destruction = 0;
        for (int j = 0; j < n; ++j) {
            if (j != i) {
                destruction += min(min(agents[j].a, agents[j].b), agents[j].c);
            }
        }

        minDestruction = min(minDestruction, destruction);
    }

    return (minDestruction != INT_MAX) ? minDestruction + 1 : -1;
}

int main() {
    int T = 1; // 테스트 케이스의 수

    for (int t = 0; t < T; ++t) {
        int n = 3; // 최정예 요원의 수


        struct Agent agents[MAX_N];

        // 최정예 요원들의 능력치 입력
        for (int i = 0; i < n; ++i) {
            agents[i].a=1;
            agents[i].b=1;
            agents[i].c=1;
        }

        // 결과 출력
        printf("#%d %d\n", t+1, calculateMinimumDestruction(agents, n));
    }

    return 0;
}
/*
int main() {
    int T; // 테스트 케이스의 수
    scanf("%d", &T);

    for (int t = 0; t < T; ++t) {
        int n; // 최정예 요원의 수
        scanf("%d", &n);

        struct Agent agents[MAX_N];

        // 최정예 요원들의 능력치 입력
        for (int i = 0; i < n; ++i) {
            scanf("%d %d %d", &agents[i].a, &agents[i].b, &agents[i].c);
        }

        // 결과 출력
        printf("#%d %d\n", t+1, calculateMinimumDestruction(agents, n));
    }

    return 0;
}
*/