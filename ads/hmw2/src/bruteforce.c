#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#define EOS '\0'

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

long int BF(char *x, int m, char *y, int n)
{
	char *yb;
	/* Searching */
	long int count = 0;
	for (yb = y; *y != EOS; ++y)
		if (memcmp(x, y, m) == 0)
			count++;
	//printf("j=%d \n",y - yb);
	return count;
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
        long int count = BF(pattern, strlen(pattern), text, n);
        printf("bf %f %ld %d %s\n", (clock() - initemps) / (double)CLOCKS_PER_SEC, count, size, pattern);
    }
    free(text);
	return 0;
}