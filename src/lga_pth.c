#include "lga_base.h"
#include "lga_pth.h"
#include <pthread.h>

typedef struct {
    byte *grid_in;
    byte *grid_out;
    int grid_size;
    int start;
    int end;
} ThreadArgs;

static void position_thread(void* arg) {
    ThreadArgs* args = (ThreadArgs*)arg;

    byte *grid_in = args->grid_in;
    byte *grid_out = args->grid_out;
    int grid_size = args->grid_size;
    int start = args->start;
    int end = args->end;

    for (int i = start; i < end; i++) {
        for (int j = 0; j < grid_size; j++) {
            for (int dir = 0; dir < NUM_DIRECTIONS; dir++) {
                byte dir_mask = 0x01 << dir;

                if (grid_in[ind2d(i, j)] & dir_mask) {
                    int di = directions[i % 2][dir][0];
                    int dj = directions[i % 2][dir][1];
                    int n_i = i + di;
                    int n_j = j + dj;

                    if (inbounds(n_i, n_j, grid_size)) {
                        if (grid_in[ind2d(n_i, n_j)] == WALL)
                            wall_collision(i, j, grid_out, grid_size, dir);
                        else
                            grid_out[ind2d(n_i, n_j)] |= dir_mask;

                        grid_in[ind2d(i, j)] &= ~dir_mask;
                    }
                }
            }
        }
    }



    pthread_exit(NULL);
}

static void collision_thread(void *arg) {
    ThreadArgs* args = (ThreadArgs*)arg;

    byte *grid_in = args->grid_in;
    byte *grid_out = args->grid_out;
    int grid_size = args->grid_size;
    int start = args->start;
    int end = args->end;

    for (int i = start; i < end; i++) {
        for (int j = 0; j < grid_size; j++) {
            grid_out[ind2d(i,j)] = particles_collision(grid_out[ind2d(i,j)]);
        }
    }

    pthread_exit(NULL);
}

static void update(byte *grid_in, byte *grid_out, int grid_size, int num_threads) {
    pthread_t threads[num_threads];
    ThreadArgs args[num_threads];

    int chunk_size = grid_size / num_threads;

    for(int i = 0; i < num_threads; i++) {
        args[i].grid_in = grid_in;
        args[i].grid_out = grid_out;
        args[i].grid_size = grid_size;
        args[i].start = i * chunk_size;
        args[i].end = (i + 1) * chunk_size;
        pthread_create(&threads[i], NULL, position_thread, (void*)&args[i]);
    }

    for(int i = 0; i < num_threads; i++)
        pthread_join(threads[i], NULL);


    for(int i = 0; i < num_threads; i++) {
        args[i].grid_in = grid_in;
        args[i].grid_out = grid_out;
        args[i].grid_size = grid_size;
        args[i].start = i * chunk_size;
        args[i].end = (i + 1) * chunk_size;
        pthread_create(&threads[i], NULL, collision_thread, (void*)&args[i]);
    }

    for(int i = 0; i < num_threads; i++)
        pthread_join(threads[i], NULL);

}

void simulate_pth(byte *grid_1, byte *grid_2, int grid_size, int num_threads) {
    for (int i = 0; i < ITERATIONS/2; i++) {
        update(grid_1, grid_2, grid_size, num_threads);
        update(grid_2, grid_1, grid_size, num_threads);
    }
}
