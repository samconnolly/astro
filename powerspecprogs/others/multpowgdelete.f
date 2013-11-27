
      character*120 title,title2
      real err(1000000)
      real oflux(100000),bflux(100000),dum,logmean
      real dff(100000),dflux(1000000)


      real dt(1000000),
      real avoflux,avofluxtot,avflux,avfluxtot
      integer i,nhi,npoints,np,nf,j,minp,minb,nptot,nbfreq



      subroutine binps(nf,freq,dff,minb,bfac,bfreq,bff,bperr,nbfreq)
      implicit none
      real freq(100000),dff(100000),bfac,flast,fprev,ffav,logftot
      real bfreq(100000),bff(100000),bperr(100000)
      integer jj,j,nbfreq,nf,minb,i,k

      jj=0
      j=0
      logftot=0.0
      ffav=0.0
      flast=bfac*freq(1)
      fprev=freq(1)  
        
      do i=1,nf
        ffav=ffav+log10(dff(i))+0.253
        j=j+1
        logftot=logftot+log10(freq(i))
        if ((freq(i+1).gt.flast.or.i.eq.nf).and.j.ge.minb) then
        jj=jj+1
        bff(jj)=ffav/real(j)
        bfreq(jj)=logftot/real(j)
        bperr(jj)=0.0
        do k=i-(j-1),i
          bperr(jj)=bperr(jj)+(log10(dff(k))+0.253-bff(jj))**2
        enddo
        bperr(jj)=sqrt(bperr(jj)/(j*real(j-1)))

        fprev=freq(i)
        flast=bfac*freq(i)
        logftot=0.0
        ffav=0.0
        j=0  
        endif
      enddo
      nbfreq=jj
        
      return        
      end

   




      subroutine sort2(n,arr,brr)
      integer n,m,nstack
      real arr(n),brr(n)
      parameter (m=7,nstack=50)
      integer i,ir,j,jstack,k,l,istack(nstack)
      real a,b,temp
      jstack=0
      l=1
      ir=n
      
 1    if (ir-l.lt.m) then
      do 12 j=l+1,ir
        a=arr(j)
        b=brr(j)
        
        do 11 i=j-1,1,-1
          if (arr(i).le.a) goto 2
          arr(i+1)=arr(i)
          brr(i+1)=brr(i)
          
 11     enddo
        i=0
 2      arr(i+1)=a
        brr(i+1)=b
        
 12   enddo
      if (jstack.eq.0) return
      ir=istack(jstack)
      l=istack(jstack-1)
      jstack=jstack-2

      else

      k=(l+ir)/2
      temp=arr(k)     
      arr(k)=arr(l+1)
      arr(l+1)=temp
      temp=brr(k)
      brr(k)=brr(l+1)
      brr(l+1)=temp

      if (arr(l+1).gt.arr(ir)) then
      temp=arr(l+1)
      arr(l+1)=arr(ir)
      arr(ir)=temp
      temp=brr(l+1)
      brr(l+1)=brr(ir)
      brr(ir)=temp
      endif

      if (arr(l).gt.arr(ir)) then
      temp=arr(l)
      arr(l)=arr(ir)
      arr(ir)=temp
      temp=brr(l)
      brr(l)=brr(ir)
      brr(ir)=temp
      endif

      if (arr(l+1).gt.arr(l)) then
      temp=arr(l+1)
      arr(l+1)=arr(l)
      arr(l)=temp
      temp=brr(l+1)
      brr(l+1)=brr(l)
      brr(l)=temp
      endif

      i=l+1
      j=ir
      a=arr(l)
      b=brr(l)

 3    continue
      i=i+1
      if (arr(i).lt.a) goto 3
 4    continue
      j=j-1
      if (arr(j).gt.a) goto 4
      if (j.lt.i) goto 5
      temp=arr(i)
      arr(i)=arr(j)
      arr(j)=temp
      temp=brr(i)
      brr(i)=brr(j)
      brr(j)=temp
      goto 3
 5    arr(l)=arr(j)
      arr(j)=a
      brr(l)=brr(j)
      brr(j)=b
      jstack=jstack+2

c.. original      if (jstack.gt.nstack) pause 'nstack too small in sort2'
c..Below, changed by IMcH, 26 April 2012 for gfortran

      if (jstack.gt.nstack) write (*,*) 'nstack too small in sort2'
      if (ir-i+1.ge.j-l) then
      istack(jstack)=ir
      istack(jstack-1)=i
      ir=j-1
      
      else
      istack(jstack)=j-1
      istack(jstack-1)=l
      l=i
      
      endif
      endif
      goto 1

      end         

