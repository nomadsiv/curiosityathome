/*
-Procedure states( Compute the state of a body relative to another )

-Abstract

   This modified version of the "cookbook" program states 
   prints coordinate and velocity data for the curiousity 
   using multiple SPK files

-Output

      - The light time and stellar aberration corrected state of
        the target body relative to the observing body plus
        the magnitude to the position and velocity vectors.

   -CSPICE Version 1.0.0, 17-OCT-1999   (EDW)

-&
*/


	/* Include needed headers. */

	#include <stdio.h>
	#include <string.h>
    #include <stdlib.h>

	#include "SpiceUsr.h"

int main (int argc, char *argv[])
{

	/*
	Local constants.
	*/

	#define     FILE_SIZE 128
	#define     WORD_SIZE 80


	/*
	Local variables.
	*/

	SpiceDouble    state[6];
	SpiceDouble    lt;
	SpiceDouble    et;
	SpiceDouble    etbeg;
	SpiceDouble    etend;
	SpiceDouble    delta;

	SpiceChar      leap  [FILE_SIZE];
	SpiceChar      spk   [FILE_SIZE];
	SpiceChar      targ  [WORD_SIZE];
	SpiceChar      obs   [WORD_SIZE];
	SpiceChar      line  [WORD_SIZE];
	SpiceChar      utcbeg[WORD_SIZE];
	SpiceChar      utcend[WORD_SIZE];
	SpiceChar      utc   [WORD_SIZE];
	SpiceChar      frame [WORD_SIZE];
	SpiceChar      abcorr[WORD_SIZE];
	SpiceChar      answer[WORD_SIZE];

	SpiceChar      format[] = "c";

	SpiceInt       maxpts   = 0;
	SpiceInt       prec     = 0;
	SpiceInt       i;

	SpiceBoolean   cont;


	furnsh_c("naif0010.tls");
	furnsh_c("de425s.bsp");
	furnsh_c("mar085s.bsp");
	furnsh_c("msl_atls_ops120808_v1.bsp");
	furnsh_c("msl_cruise_v1.bsp");
	furnsh_c("msl_ls_ops120808_iau2000_v1.bsp");
	furnsh_c("msl_struct_v02.bsp");
	furnsh_c("msl_surf_rover_tlm_0000_0089_v1.bsp");
	furnsh_c("msl_v06.tf");
	furnsh_c("pck00008.tpc");
	                         
	/* set observer to MSL and set target to MARS */
	strcpy(obs,"MSL");
	strcpy(targ,"MSL_LANDING_SITE");

	if (argc < 2) {
		printf("usage %s (iterations in number)\n",argv[0]);
		return(1);
			
	}else{
		maxpts=atoi(argv[1]);
	}

  

	while ( maxpts <= 0 );


	/* Query for the time interval. */
	strcpy(utcbeg,"2012-08-30T12");
	strcpy(utcend,"2012-09-30T12");
	/*if ( maxpts == 1 ) {
		prompt_c ( "Enter the UTC time (default=2012-08-30T12): ", WORD_SIZE, utcbeg );
		puts(" ");
	} else {
		prompt_c ( "Enter the beginning UTC time:(default=2012-08-30T12) ", WORD_SIZE, utcbeg );
	puts(" ");

      prompt_c ( "Enter the ending UTC time: ",    WORD_SIZE, utcend );
      puts(" ");
      }
	*/
	
	/* reference frame set to j2000 */
	strcpy(frame,"J2000");
	/* set correction to NONE */
	strcpy(abcorr,"NONE");
	  
	/*
	Convert the UTC time strings into DOUBLE PRECISION ETs.
	*/
   
	if ( maxpts == 1 ) {
		str2et_c ( utcbeg, &etbeg );
	}else {
		str2et_c ( utcbeg, &etbeg );
		str2et_c ( utcend, &etend );
	}

   /*
   At each time, compute and print the state of the target body
   as seen by the observer.  The output time will be in calendar
   format, rounded to the nearest seconds.

   delta is the increment between consecutive times.

   Make sure that the number of points is >= 1, to avoid a
   division by zero error.
   */

	if ( maxpts > 1 ) {
		delta  = ( etend - etbeg ) / ( (SpiceDouble) maxpts - 1.);
	}else{
		delta = 0.0;
	}


	/* Initialize control variable for the spkezr_c loop. */
	et   = etbeg;
	cont = SPICETRUE;
	i    = 1;

	/*
	Perform the state look ups for the number of requested 
	intervals. The loop continues so long as the expression:

            i <= maxpts  &&  cont == SPICETRUE

	evaluates to true.
	*/
   
	do{
      /*
      Compute the state of 'targ' from 'obs' at 'et' in the 'frame'
      reference frame and aberration correction 'abcorr'.
      */
      spkezr_c ( targ, et, frame, abcorr, obs, state, &lt );

      /*
      Convert the ET (ephemeris time) into a UTC time string
      for displaying on the screen.
      */
      et2utc_c ( et, format, prec, WORD_SIZE, utc );

      /* 
      Display the results of the state calculation.
      */
      printf ( "For time %d of %d, the state of:\n", i, maxpts );

      printf ( "Body            : %s\n", targ );

      printf ( "Relative to body: %s\n", obs );

      printf ( "In Frame        : %s\n", frame );

      printf ( "At UTC time     : %s\n", utc );

      puts  (" ");
      printf( "                 Position (km)              ");
      printf( "Velocity (km/s)\n"                           );
      printf( "            -----------------------     "    );
      printf( "-----------------------\n" );

      printf( "          X: %23.16e     %26.16e\n", state[0],
                                                    state[3] );
      printf( "          Y: %23.16e     %26.16e\n", state[1],
                                                    state[4] );
      printf( "          Z: %23.16e     %26.16e\n", state[2],
                                                    state[5] );
      printf( "  MAGNITUDE: %23.16e     %23.16e\n", 
                                                vnorm_c(state),
                                                vnorm_c(state+3) );

      /* One output cycle finished. Continue? */ 
     
      //   cont = SPICEFALSE;
      
      /*
      Increment the current et by delta and increment the loop
      counter to mark the next cycle.
      */
      et = et + delta;
      i = i + 1;

      }while ( i <= maxpts  &&  cont == SPICETRUE );


   /* Finis */
   return ( 0 );
}
