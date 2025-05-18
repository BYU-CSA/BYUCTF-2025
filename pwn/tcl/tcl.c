#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <pthread.h>
#include <unistd.h>

enum {
    TYPE_FLOAT = 0,
    TYPE_INT,
    TYPE_STRING,
    TYPE_BOOL,
};

struct str_object {
    char *value;
    unsigned int type;
    unsigned int refcount;
};

struct int_object {
    unsigned long value;
    unsigned int type;
    unsigned int refcount;
};

struct float_object {
    double value;
    unsigned int type;
    unsigned int refcount;
};

struct bool_object {
    unsigned long value;
    unsigned int type;
    unsigned int refcount;
};

void* objects[100];

__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void win() {
    system("/bin/sh");
    exit(0);
}

int create_string_obj(char *value) {
    struct str_object* obj = (struct str_object*)objects[0];
    unsigned int i = 0;

    // if the object already exists, just increase the refcount
    while (obj != NULL) {
        if ((obj->type == TYPE_STRING) && (strcmp(obj->value, value) == 0)) {
            printf("Added refcount to %s\n", obj->value);
            obj->refcount++;
            return 0;
        }
        if (i >= 99) {
            puts("object array is full");
            return -1;
        }
        i++;
        obj = (struct str_object*)objects[i];
    }

    // otherwise, create a new object
    obj = (struct str_object*)malloc(sizeof(struct str_object));
    if (obj == NULL) {
        puts("malloc failed");
        exit(1);
    }
    obj->value = strdup(value);
    if (obj->value == NULL) {
        puts("strdup failed");
        exit(1);
    }
    obj->type = TYPE_STRING;
    obj->refcount = 1;
    objects[i] = obj;
    return 0;
}

int create_int_obj(unsigned long value) {
    struct int_object* obj = (struct int_object*)objects[0];
    unsigned int i = 0;

    // if the object already exists, just increase the refcount
    while (obj != NULL) {
        if ((obj->type == TYPE_INT) && (obj->value == value)) {
            printf("Added refcount to %lu\n", obj->value);
            obj->refcount++;
            return 0;
        }
        if (i >= 99) {
            puts("object array is full");
            return -1;
        }
        i++;
        obj = (struct int_object*)objects[i];
    }

    // otherwise, create a new object
    obj = (struct int_object*)malloc(sizeof(struct int_object));
    if (obj == NULL) {
        puts("malloc failed");
        exit(1);
    }
    obj->value = value;
    obj->type = TYPE_INT;
    obj->refcount = 1;
    objects[i] = obj;
    return 0;
}

int create_float_obj(double value) {
    struct float_object* obj = (struct float_object*)objects[0];
    unsigned int i = 0;

    // if the object already exists, just increase the refcount
    while (obj != NULL) {
        if ((obj->type == TYPE_FLOAT) && (obj->value == value)) {
            printf("Added refcount to %lf\n", obj->value);
            obj->refcount++;
            return 0;
        }
        if (i >= 99) {
            puts("object array is full");
            return -1;
        }
        i++;
        obj = (struct float_object*)objects[i];
    }

    // otherwise, create a new object
    obj = (struct float_object*)malloc(sizeof(struct float_object));
    if (obj == NULL) {
        puts("malloc failed");
        exit(1);
    }
    obj->value = value;
    obj->type = TYPE_FLOAT;
    obj->refcount = 1;
    objects[i] = obj;
    return 0;
}

int create_bool_obj(unsigned long value) {
    struct bool_object* obj = (struct bool_object*)objects[0];
    unsigned int i = 0;

    // if the object already exists, just increase the refcount
    while (obj != NULL) {
        if ((obj->type == TYPE_BOOL) && (obj->value == value)) {
            printf("Added refcount to %lu\n", obj->value);
            obj->refcount++;
            return 0;
        }
        if (i >= 99) {
            puts("object array is full");
            return -1;
        }
        i++;
        obj = (struct bool_object*)objects[i];
    }

    // otherwise, create a new object
    obj = (struct bool_object*)malloc(sizeof(struct bool_object));
    if (obj == NULL) {
        puts("malloc failed");
        exit(1);
    }
    obj->value = value;
    obj->type = TYPE_BOOL;
    obj->refcount = 1;
    objects[i] = obj;
    return 0;
}

void clear_objects() {
    for (unsigned int i = 0; i < 100; i++) {
        if (objects[i] != NULL) {
            // set refcount to 0 for the garbage collector to free
            struct str_object* obj = (struct str_object*)objects[i];
            obj->refcount = 0;
        }
    }
}

void parse_tcl() {
    char buf[0x100];
    bool valid = true;
    bool started = false;

    while (1) {
        // clear the buffer
        memset(buf, 0, sizeof(buf));

        // we use fgets because it breaks on \n, which means the config line is done
        fgets(buf, sizeof(buf), stdin);

        // remove the newline character
        size_t len = strlen(buf);
        if (len > 0 && buf[len - 1] == '\n') {
            buf[len - 1] = '\0';
        }
        // check for empty line
        if (strlen(buf) == 0) {
            continue;
        }

        if (started == false) {
            // check for the start of the config
            if (strcmp(buf, "#START") != 0) {
                puts("You need to start with #START");
                continue;
            }
            started = true;
            continue;
        }

        if (strcmp(buf, "#END") == 0) {
            break;
        }

        // check for ' = '
        char * delim = strstr(buf, " = ");
        if (delim == NULL) {
            puts("Invalid line, no ' = ' found");
            valid = false;
            continue;
        }
        *delim = '\0'; // replace ' = ' with '\0' to split the string
        delim += 3; // move past the ' = '
        // at this point, buf contains the key name and delim points to the value

        // ensure first character is not a digit
        if (isdigit(buf[0])) {
            puts("Key name cannot start with a digit");
            valid = false;
            continue;
        }

        // check character set in keyname
        for (char *p = buf; *p != '\0'; p++) {
            if (!isalnum(*p) && *p != '_') {
                puts("Key name can only contain alphanumeric characters and underscores");
                valid = false;
                continue;
            }
        }

        // create an object to store key name
        if (create_string_obj(buf) != 0) {
            puts("create_string_obj failed");
            valid = false;
            continue;
        }

        // CHECK THE VALUE NOW

        // inspecting the first character of the value will tell us what type it is
        if (isdigit(delim[0])) {
            // it's an int or float
            char *endptr;
            unsigned long value = strtoul(delim, &endptr, 10);
            if (*endptr == '.') {
                // it's a float
                double fvalue = strtod(delim, NULL);
                if (create_float_obj(fvalue) != 0) {
                    puts("create_float_obj failed");
                    valid = false;
                    continue;
                }
            } else {
                // it's an int
                if (create_int_obj(value) != 0) {
                    puts("create_int_obj failed");
                    valid = false;
                    continue;
                }
            }
        }

        else if (delim[0] == 't' || delim[0] == 'f') {
            if (strcmp(delim, "true") != 0 && strcmp(delim, "false") != 0) {
                puts("Invalid boolean value");
                valid = false;
                continue;
            }

            // it's a bool
            unsigned long value = (delim[0] == 't') ? 1 : 0;
            if (create_bool_obj(value) != 0) {
                puts("create_bool_obj failed");
                valid = false;
                continue;
            }
        }

        else if (delim[0] == '"') {
            // it's a string
            delim++; // move past the opening quote
            char *end = strchr(delim, '"');
            if (end == NULL) {
                puts("Invalid string value, no closing quote found");
                valid = false;
                continue;
            }
            *end = '\0'; // replace closing quote with null terminator
            if (create_string_obj(delim) != 0) {
                puts("create_string_obj failed");
                valid = false;
                continue;
            }
        }

        else {
            // invalid value type
            puts("Invalid value type");
            valid = false;
            continue;
        }
    }

    // check if the config is valid
    if (valid) {
        puts("Config is valid");
    } else {
        puts("Config is invalid");
    }

    // set the refcount of all objects to 0
    clear_objects();
}

void gc() {
    unsigned int indexes[100];
    unsigned int count = 0;

    while (1) {
        memset(indexes, 0, sizeof(indexes));
        count = 0;
        sleep(5);

        // store the indexes of all objects with refcount 0
        for (unsigned int i = 0; i < 100; i++) {
            if (objects[i] != NULL) {
                struct str_object* obj = (struct str_object*)objects[i];
                if (obj->refcount == 0) {
                    indexes[count++] = i;
                }
            }
        }

        // free them
        for (unsigned int i = 0; i < count; i++) {
            struct str_object* obj = (struct str_object*)objects[indexes[i]];
            if (obj != NULL) {
                if (obj->type == TYPE_STRING)
                    free(obj->value);
                free(obj);
                usleep(5 * 1000); // sleep for 5 milliseconds - we don't want to hog the CPU!
            }
        }

        // set the object pointer to NULL
        for (unsigned int i = 0; i < count; i++) {
            struct str_object* obj = (struct str_object*)objects[indexes[i]];
            // double check refcount is 0 before setting to NULL
            if (obj != NULL && obj->refcount == 0) {
                objects[indexes[i]] = NULL;
            }
        }
    }
}

int main() {
    alarm(60); // set a timeout for the program
    printf("%p\n", &alarm);

    // spawn garbage collector
    pthread_t tid;
    pthread_create(&tid, NULL, (void*)gc, NULL);

    while (1) {
        puts("Enter your TCL file contents below:");
        puts("=========================================");
        parse_tcl();
    }

    return 0;
}