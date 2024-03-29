#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define FALSE 0
#define TRUE 1
#define UNDEFINED -1

struct _cell{
    int element;
    struct _cell *next;
};

typedef struct _cell *List;

int getTransition(char *x, int p, List L[], char c)
{
    List cell;

    if (p > 0 && x[p - 1] == c)
        return (p - 1);
    else
    {
        cell = L[p];
        while (cell != NULL)
            if (x[cell->element] == c)
                return (cell->element);
            else
                cell = cell->next;
        return (UNDEFINED);
    }
}

void setTransition(int p, int q, List L[])
{
    List cell;

    cell = (List)malloc(sizeof(struct _cell));
    if (cell == NULL)
        printf("BOM/setTransition");
    cell->element = q;
    cell->next = L[p];
    L[p] = cell;
}

void oracle(char *x, int m, char T[], List L[])
{
    int i, p, q;
    int S[m + 1];
    char c;

    S[m] = m + 1;
    for (i = m; i > 0; --i)
    {
        c = x[i - 1];
        p = S[i];
        while (p <= m &&
                (q = getTransition(x, p, L, c)) ==
                    UNDEFINED)
        {
            setTransition(p, i - 1, L);
            p = S[p];
        }
        S[i - 1] = (p == m + 1 ? m : q);
    }
    p = 0;
    while (p <= m)
    {
        T[p] = TRUE;
        p = S[p];
    }
}

long int BOM(char *x, int m, char *y, int n)
{
    char T[m + 1];
    List L[m + 1];
    int i, j, p, period, q, shift;

    /* Preprocessing */
    memset(L, NULL, (m + 1) * sizeof(List));
    memset(T, FALSE, (m + 1) * sizeof(char));
    oracle(x, m, T, L);

    /* Searching */
    j = 0;
    long int count = 0;
    while (j <= n - m)
    {
        i = m - 1;
        p = m;
        shift = m;
        while (i + j >= 0 &&
                    (q = getTransition(x, p, L, y[i + j])) !=
                        UNDEFINED)
        {
            p = q;
            if (T[p] == TRUE)
            {
                period = shift;
                shift = i;
            }
            --i;
        }
        if (i < 0)
        {
            ++count;
            shift = period;
        }
        j += shift;
    }
    return count;
}

long readfile(char *filename, char *text[])
{
	FILE *fin;
	long len;
	int i = 0;
	char c;

	if (!(fin = fopen(filename, "r")))
	{
		fprintf(stderr, "I can't open the file: %s\n", filename);
		exit(1);
	}
	// llegim el nombre de caracters que hi ha al fitxer
	fseek(fin, 0, SEEK_END);
	len = ftell(fin);
	fseek(fin, 0, SEEK_SET);
	// demanem memoria per la variable text
	*text = malloc(len + 1);
	// bucle per llegir el fitxer
	while ((c = (fgetc(fin))) != EOF)
	{
		if ((c == 'a') || (c == 'c') || (c == 'g') || (c == 't') || (c == 'A') || (c == 'C') || (c == 'G') || (c == 'T'))
		{
			(*text)[i] = c;
			//printf("text[%d] = %c\n", i, (*text)[i]);
			i++;
		}
	}
	fclose(fin);
	return i;
}

int main(int argc, char *argv[])
{

	char filename[256];
	char *text;
    int n, size;
    clock_t initemps;
	sprintf(filename, "%s", argv[1]);
    n = readfile(filename, &text);

    for (int i = 2; i < argc; i += 2) {
        size = atoi(argv[i]);
        char pattern[size];
        sprintf(pattern, "%s", argv[i+1]);

        initemps = clock();
        long int count = BOM(pattern, strlen(pattern), text, n);
        printf("bom %f %ld %d %s\n", (clock() - initemps) / (double)CLOCKS_PER_SEC, count, size, pattern);
    }
    free(text);
	return 0;
}
