#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include "mapreduce.h"
#include "hashmap.h"
#include <pthread.h>

struct kv
{
    char *key;
    char *value;
};

struct kv_list
{
    struct kv **elements;
    size_t num_elements;
    size_t size;
};

typedef struct
{
    Mapper *map;
    char *filename;
} map_args_t;

typedef struct
{
    Reducer *reduce;
    Getter get;
    char *key;
    int partition_number;
} reduce_args_t;

int num_partitions;
struct kv_list **kv_partitions;
int *counters;
Partitioner the_partition;

void init_kv_list(size_t size, struct kv_list *partition)
{
    (*(partition)).elements = (struct kv **)malloc(size * sizeof(struct kv *));
    (*(partition)).num_elements = 0;
    (*(partition)).size = size;
}

void add_to_list(struct kv_list *partition, struct kv *elt)
{

    if ((*(partition)).num_elements == (*(partition)).size)
    {
        (*(partition)).size *= 2;
        (*(partition)).elements = realloc((*(partition)).elements, (*(partition)).size * sizeof(struct kv *));
    }
    (*(partition)).elements[(*(partition)).num_elements++] = elt;
}
char *get_func(char *key, int partition_number)
{
    struct kv_list *curr_partition = kv_partitions[partition_number];
    struct kv *curr_elt = curr_partition->elements[counters[partition_number]];

    if (curr_elt == NULL)
    {
        return NULL;
    }
    if (!strcmp(curr_elt->key, key))
    {
        counters[partition_number]++;
        return curr_elt->value;
    }
    return NULL;
}
// compare two
int cmp(const void *a, const void *b)
{
    char *str1 = (*(struct kv **)a)->key;
    char *str2 = (*(struct kv **)b)->key;
    return strcmp(str1, str2);
}
unsigned long MR_DefaultHashPartition(char *key, int num_partitions)
{
    unsigned long hash = 5381;
    int c;
    while ((c = *key++) != '\0')
    {
        hash = hash * 33 + c;
    }
    return hash % num_partitions;
}
void MR_Emit(char *key, char *value)
{
    int partition = the_partition(key, num_partitions);
    struct kv *elt = (struct kv *)malloc(sizeof(struct kv));
    if (elt == NULL)
    {
        printf("Malloc error! %s\n", strerror(errno));
        exit(1);
    }
    elt->key = strdup(key);
    elt->value = strdup(value);
    pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
    pthread_mutex_lock(&lock);
    add_to_list(kv_partitions[partition], elt);
    pthread_mutex_unlock(&lock);
    return;
}
void *myMap(void *args)
{
    map_args_t *mapArgs = (map_args_t *)args;
    (*(mapArgs->map))(mapArgs->filename);
    return NULL;
}

void *myReduce(void *args)
{
    reduce_args_t *reduceArgs = (reduce_args_t *)args;
    (*(reduceArgs->reduce))(reduceArgs->key, reduceArgs->get, reduceArgs->partition_number);
    return NULL;
}
void printPartitions(int num_partitions)
{
    char *key = "";
    char *value = "";
    printf("Printing %d partitions:\n", num_partitions);
    for (int i = 0; i < num_partitions; ++i)
    {
        printf("[partitions[%d]: \n", i);
        for (int j = 0; j < kv_partitions[i]->num_elements; ++j)
        {
            key = kv_partitions[i]->elements[j]->key;
            value = kv_partitions[i]->elements[j]->value;
            printf("\t<k,v>: <%s,%s>\n", key, value);
        }
    }
}
int numberOfKey(char *key, int partition_number)
{
    int count = 0;
    char *keytoCompare = "";
    for (int i = 0; i < kv_partitions[partition_number]->num_elements; ++i)
    {
        keytoCompare = kv_partitions[partition_number]->elements[i]->key;
        if (strcmp(key, keytoCompare) == 0)
        {
            count++;
        }
    }
    return count;
}
int numberOfDistinctKeys()
{
    int curr_part = 0;
    int curr_key = 0;
    int distinctkeys = 0;
    if (kv_partitions[curr_part]->num_elements == 0)
    {
        while ((kv_partitions[curr_part]->num_elements == 0) && (curr_part < num_partitions))
        {
            curr_part++;
        }
    }
    while (curr_part < num_partitions && curr_key < kv_partitions[curr_part]->num_elements)
    {
        int numberOfCurrKey = numberOfKey(kv_partitions[curr_part]->elements[curr_key]->key, curr_part);
        distinctkeys++;
        curr_key += numberOfCurrKey;
        if (curr_key == kv_partitions[curr_part]->num_elements)
        {
            curr_part++;
            curr_key = 0;
        }
        if (curr_part == num_partitions)
        {
            break;
        }
        if (kv_partitions[curr_part]->num_elements == 0)
        {
            while (kv_partitions[curr_part]->num_elements == 0)
            {
                curr_part++;
            }
        }
        if (curr_part == num_partitions)
        {
            break;
        }
    }
    return distinctkeys;
}

void MR_Run(int argc, char *argv[], Mapper map, int num_mappers, Reducer reduce, int num_reducers, Partitioner partition)
{
    map_args_t myMapArgs = {&map, ""};
    pthread_t mapthreads[num_mappers];
    memset(mapthreads, 0, num_mappers * sizeof(pthread_t));
    the_partition = partition;
    num_partitions = num_reducers;
    counters = malloc(num_partitions * sizeof(int));
    kv_partitions = (struct kv_list **)malloc(num_partitions * sizeof(struct kv_list *));
    for (int i = 0; i < num_partitions; ++i)
    {
        counters[i] = 0;
        kv_partitions[i] = malloc(10 * sizeof(struct kv_list));
        init_kv_list(10, kv_partitions[i]);
    }
    int num_files = argc - 1;
    int files_leftover = num_files - num_mappers;
    int curr_mapper = 0;
    int curr_file = 0;
    while (curr_mapper < num_mappers && curr_file < num_files)
    {
        myMapArgs.filename = argv[curr_file + 1];
        curr_file++;
        int rc = pthread_create(&mapthreads[curr_mapper], NULL, myMap, &myMapArgs);
        if (rc != 0)
        {
            printf("Thread creation failed\n");
            fflush(stdout);
        }
        pthread_join(mapthreads[curr_mapper], NULL);
        curr_mapper++;
        if (curr_mapper == num_mappers)
        {
            if (curr_file < num_files)
            {
                curr_mapper -= files_leftover;
                if (curr_mapper < 0)
                {
                    curr_mapper = 0;
                }
            }
        }
    }
    for (int i = 0; i < num_partitions; ++i)
    {
        qsort(kv_partitions[i]->elements, kv_partitions[i]->num_elements, sizeof(struct kv *), cmp);
    }
    pthread_t reducerthreads[num_reducers];
    memset(reducerthreads, 0, num_reducers * sizeof(pthread_t));
    reduce_args_t myReduceArgs = {&reduce, get_func, "", 0};
    int num_distinct_keys = numberOfDistinctKeys();
    int keys_leftover = num_distinct_keys - num_reducers;
    int curr_reducer = 0;
    int curr_distinct_key = 0;
    int curr_key_index = 0;
    int curr_partition = 0;
    if (kv_partitions[curr_partition]->num_elements == 0)
    {
        while ((kv_partitions[curr_partition]->num_elements == 0) && (curr_partition < num_partitions))
        {
            curr_partition++;
        }
    }
    while (curr_reducer < num_reducers && curr_distinct_key < num_distinct_keys)
    {
        myReduceArgs.key = kv_partitions[curr_partition]->elements[curr_key_index]->key;
        myReduceArgs.partition_number = curr_partition;
        curr_distinct_key++;
        int rc = pthread_create(&reducerthreads[curr_reducer], NULL, myReduce, &myReduceArgs);
        if (rc != 0)
        {
            printf("Thread creation failed\n");
            fflush(stdout);
        }
        pthread_join(reducerthreads[curr_reducer], NULL);
        curr_key_index += numberOfKey(myReduceArgs.key, curr_partition);
        if (curr_key_index == kv_partitions[curr_partition]->num_elements)
        {
            curr_partition++;
            curr_key_index = 0;
            if (curr_partition == num_partitions)
            {
                break;
            }
            if (kv_partitions[curr_partition]->num_elements == 0)
            {
                while (kv_partitions[curr_partition]->num_elements == 0 && curr_partition < num_partitions)
                {
                    curr_partition++;
                }
            }
        }
        curr_reducer++;
        if (curr_reducer == num_reducers)
        {
            if (curr_distinct_key < num_distinct_keys)
            {
                curr_reducer -= keys_leftover;
                if (curr_reducer < 0)
                {
                    curr_reducer = 0;
                }
            }
        }
    }

    for (int i = 0; i < num_partitions; ++i)
    {
        for (int j = 0; j < kv_partitions[i]->num_elements; ++j)
        {
            free(kv_partitions[i]->elements[j]);
        }
        free(kv_partitions[i]->elements);
        free(kv_partitions[i]);
    }
    free(counters);
    free(kv_partitions);
}
