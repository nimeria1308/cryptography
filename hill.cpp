#include <iostream>
#include <string.h>

using namespace std;

// assume alphabet encoding A -> 0, ..., Z -> 25
static inline void message_to_numbers(
    const char *message, unsigned int *vector)
{
    size_t len = strlen(message);
    for (size_t i = 0; i < len; i++)
    {
        vector[i] = message[i] - 'A';
    }
}

static inline void numbers_to_message(
    const unsigned int *vector, char *message, size_t len)
{
    for (size_t i = 0; i < len; i++)
    {
        message[i] = 'A' + vector[i];
    }

    // C string is NULL terminated
    message[len] = 0;
}

static inline void print_numbers(const unsigned int *vector, size_t len)
{
    cout << "{ ";

    for (size_t i = 0; i < len; i++)
    {
        cout << "{" << vector[i] << "}, ";
    }

    cout << "}" << endl;
}

template <size_t size>
static inline void encode(
    const unsigned int *key,
    const unsigned int *input_vector,
    unsigned int *output_vector)
{
    memset(output_vector, 0, sizeof(*output_vector) * size);
    for (size_t i = 0; i < size; i++)
    {
        // cout << i << ": " << output_vector[i] << endl;
        for (size_t j = 0; j < size; j++)
        {
            output_vector[i] += *key++ * input_vector[j];
        }
        output_vector[i] %= 26;
    }
}

/*
Solve[{
M3. {{2}, {17}, {24}} == { {21}, {6}, {24}},
M3.{{15}, {19}, {14}}=={{23}, {0}, {17}},
M3.{{6}, {17}, {0}}=={{3}, {8}, {6}},
M3.{{15}, {7}, {24}}=={{11}, {12}, {11}}
}, {a,b,c,d,e,f,g,h,i}, Modulus->26]

{{a->2,b->1,c->0,d->0,e->2,f->1,g->1,h->0,i->2},{a->2,b->1,c->13,d->0,e->2,f->1,g->1,h->0,i->2},{a->2,b->1,c->0,d->0,e->2,f->14,g->1,h->0,i->2},{a->2,b->1,c->13,d->0,e->2,f->14,g->1,h->0,i->2},{a->2,b->1,c->0,d->0,e->2,f->1,g->1,h->0,i->15},{a->2,b->1,c->13,d->0,e->2,f->1,g->1,h->0,i->15},{a->2,b->1,c->0,d->0,e->2,f->14,g->1,h->0,i->15},{a->2,b->1,c->13,d->0,e->2,f->14,g->1,h->0,i->15}}
*/

template <size_t size>
static inline void find_keys_(
    unsigned int *key,
    size_t key_index,
    const unsigned int *input_vector,
    const unsigned int *output_vector)
{
    if (key_index < (size * size))
    {
        for (unsigned int i = 0; i < 26; i++)
        {
            key[key_index] = i;
            find_keys_<size>(key, key_index + 1, input_vector, output_vector);
        }
    }
    else
    {
        // reached leaf
        unsigned int reencoded[size];
        char message[size + 1];
        encode<size>(key, input_vector, reencoded);
        // numbers_to_message(reencoded, message, size);
        // cout << message << endl;

        if (!memcmp(reencoded, output_vector, size * sizeof(unsigned int)))
        {
            for (int i = 0; i < 2; i++)
            {
                numbers_to_message(&output_vector[i * size], message, size);
                cout << message;
            }
            cout << " ";
            for (int i = 0; i < 2; i++)
            {
                encode<size>(key, &input_vector[i * size], reencoded);
                numbers_to_message(reencoded, message, size);
                cout << message;
            }
            // for (size_t s = 0; s < (size * 2); s++)
            // {
            //     cout << " " << key[s];
            // }

            cout << endl;
        }
    }
}

template <size_t size>
static inline void find_keys(
    const unsigned int *input_vector,
    const unsigned int *output_vector)
{
    unsigned int key[size * size];
    find_keys_<size>(key, 0, input_vector, output_vector);
    cout << "THats all folks" << endl;
}

int main()
{
    const char *plain_text = "CRYPTOGRAPHY";
    const char *cipher_text = "VGYXARDIGLML";

    unsigned int input_vector[12];
    message_to_numbers(plain_text, input_vector);
    print_numbers(input_vector, 12);

    unsigned int output_vector[12];
    message_to_numbers(cipher_text, output_vector);
    print_numbers(output_vector, 12);

#if 0
    // {2}, {17}
    // {21}, {6}
    // 2 * a + 17 * b = 21
    // 2 * c + 17 * d = 6 // 32 // 58
    char message[13] = {0};
    const unsigned int key[] = {2, 1, 12, 2};
    numbers_to_message(key, message, 4);
    cout << "key: " << message << endl;

    // 2*2 + 17*1
    // 2*12 + 17*2

    // cout << "Message: ";
    // for (size_t i = 0; i < (12 / 2); i++)
    // {
    //     encode<2>(key, &input_vector[i * 2], output_vector);
    //     numbers_to_message(output_vector, message, 2);
    //     cout << message;
    // }
    // cout << endl;

    find_keys<2>(input_vector, output_vector);
#endif
    // const unsigned int key[] = {2, 1, 0,  0, 2, 1,  1, 0, 2 };
    // const unsigned int key[] = {2, 1, 13, 0, 2, 1,  1, 0, 2 };
    // const unsigned int key[] = {2, 1, 0,  0, 2, 14, 1, 0, 2 };
    // const unsigned int key[] = {2, 1, 13, 0, 2, 14, 1, 0, 2 };
    // const unsigned int key[] = {2, 1, 0,  0, 2, 1,  1, 0, 15};
    // const unsigned int key[] = {2, 1, 13, 0, 2, 1,  1, 0, 15};
    // const unsigned int key[] = {2, 1, 0,  0, 2, 14, 1, 0, 15};
    const unsigned int key[] = {2, 1, 13, 0, 2, 14, 1, 0, 15};

    // 2, 1, 0/13, 0, 2, 1/14, 1, 0, 2/15

    // VGYXARDIGLML
    // VGYGLVLXKXAR
    char key_message[10];
    numbers_to_message(key, key_message, 9);
    cout << "Key: " << key_message << endl;

    cout << "Reconstructed cypher: ";
    for (size_t i = 0; i < 4; i++)
    {
        unsigned int reconstructed_cypher[3] = {0};
        char reconstructed_cypher_message[4] = {0};

        encode<3>(key, &input_vector[i], reconstructed_cypher);
        numbers_to_message(reconstructed_cypher, reconstructed_cypher_message, 3);
        cout << reconstructed_cypher_message;
    }
    cout << endl;
    return 0;
}
