
/*
 * Copyright 2006, Naoki Takebayashi <ffnt@uaf.edu>
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 * 02110-1301 USA
 */

#include <stdio.h>
#include <stdint.h> /* for int64_t etc */
#include <limits.h>

int
main(void)
{
  unsigned long long llmax;
  long long llmin;
  int i;

  printf("The sizes of some fundamental types are printed.\n\n");
  printf("                  char: %3d byte (%d to %d)\n", 
   sizeof(char), CHAR_MIN, CHAR_MAX);
  printf("           signed char: %3d byte (%d to %d)\n",
   sizeof(signed char), SCHAR_MIN, SCHAR_MAX);
  printf("         unsigned char: %3d byte (%d to %d)\n",
     sizeof(unsigned char), 0, UCHAR_MAX);
  printf("      signed short int: %3d byte (%d to %d)\n",
   sizeof(signed short int), SHRT_MIN, SHRT_MAX);
  printf("    unsigned short int: %3d byte (%d to %d)\n",
   sizeof(unsigned short int), 0, USHRT_MAX);
  printf("            signed int: %3d byte (%d to %d)\n",
   sizeof(signed int), INT_MIN, INT_MAX);
  printf("          unsigned int: %3d byte (%d to %u)\n",
   sizeof(unsigned int), 0, UINT_MAX);
  printf("       signed long int: %3d byte (%ld to %ld)\n", 
   sizeof(signed long int), LONG_MIN, LONG_MAX);
  printf("     unsigned long int: %3d byte (%d to %lu)\n",
   sizeof(unsigned long int), 0,ULONG_MAX);

#ifdef LLONG_MAX
  printf("  signed long long int: %3d byte (%lld to %lld)\n", 
   sizeof(signed long long),LLONG_MIN, LONG_LONG_MAX);
#else
  llmax=1;
  for (i = 0; i < (sizeof(signed long long) * 8 - 1); i++ )
    llmax *= 2 ;
  llmax --;
    
  llmin = - llmax - 1LL;
  printf("  signed long long int: %3d byte (%lld to %llu)\n",
   sizeof(signed long long), llmin,  llmax);
#endif  

#ifdef ULLONG_MAX
  printf("unsigned long long int: %3d byte (%d to %llu)\n", 
   sizeof(unsigned long long), 0, ULLONG_MAX);
#else
  printf("unsigned long long int: %3d byte (%d to %llu)\n", 
     sizeof(unsigned long long), 0, -1LL);
#endif
  printf("               int32_t: %3d byte \n", sizeof(int32_t));
  printf("              uint32_t: %3d byte \n", sizeof(uint32_t));
  printf("               int64_t: %3d byte \n", sizeof(int64_t));
  printf("              uint64_t: %3d byte \n", sizeof(uint64_t));
  
  printf("                 float: %3d byte \n", sizeof(float));
  printf("                double: %3d byte \n", sizeof(double));
  printf("           long double: %3d byte \n", sizeof(long double));
  
  printf("                 int *: %3d byte \n", sizeof(int *));
  printf("         long double *: %3d byte \n", sizeof(long double *));
  
  return(0);
}
