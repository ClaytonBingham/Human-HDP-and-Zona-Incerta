#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _AXNODE_reg(void);
extern void _AXNODEX_reg(void);
extern void _na12_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"AXNODE.mod\"");
    fprintf(stderr," \"AXNODEX.mod\"");
    fprintf(stderr," \"na12.mod\"");
    fprintf(stderr, "\n");
  }
  _AXNODE_reg();
  _AXNODEX_reg();
  _na12_reg();
}
