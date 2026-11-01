// Every exported frame is a pure function of t. No network or real-time animation state.
const PAPER='#efe5d3', INK='#121315', RED='#e5364f', ROSE='#ff8793';
const clamp=x=>Math.max(0,Math.min(1,x));
const mix=(a,b,p)=>a+(b-a)*p;
const ease=x=>{x=clamp(x);return x*x*x*(10+x*(-15+6*x))};
const E=(t,a,b)=>ease((t-a)/(b-a));
const appear=(t,a,b,c,d)=>E(t,a,b)*(1-E(t,c,d));
const num=n=>Number(n).toFixed(3);
function group(content,transform='',opacity=1){return opacity<=0?'':`<g opacity="${num(opacity)}" transform="${transform}">${content}</g>`}
function line(d,p=1,color=PAPER,width=3.4,opacity=1){
 if(p<=0||opacity<=0)return '';
 const dash=p>=.999999?'':`pathLength="1" stroke-dasharray="1" stroke-dashoffset="${num(1-clamp(p))}"`;
 return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${dash} opacity="${num(opacity)}" vector-effect="non-scaling-stroke"/>`;
}
function display(text,x,y,size,color=PAPER,opacity=1,extra=''){
 return `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" opacity="${num(opacity)}" ${extra}>${text}</text>`;
}
function handPath(str,x,y,scale=1){
 let d='',cursor=0;
 for(const ch of str){
  if(ch===' '){d+=` C${x+(cursor+19)*scale} ${y+81*scale} ${x+(cursor+49)*scale} ${y+81*scale} ${x+(cursor+71)*scale} ${y+76*scale}`;cursor+=71;continue;}
  const [w,source]=GL[ch]||GL[ch.toLowerCase()];
  let isX=true;const path=source.replace(/-?\d+(?:\.\d+)?/g,s=>{const v=Number(s);const n=isX?x+(cursor+v)*scale:y+v*scale;isX=!isX;return num(n)});
  d+=(d?' ':`M${x} ${y+76*scale} `)+path;cursor+=w;
 }
 return {d,end:[x+cursor*scale,y+76*scale]};
}
function hand(str,x,y,scale,p,color=PAPER){return line(handPath(str,x,y,scale).d,p,color,3.3)}
const HAT='M-240 105 C-195 72 -126 32 -84 0 C-43 -62 -14 -198 32 -282 C51 -246 52 -219 91 -196 L121 -216 C125 -163 88 -108 116 -34 L150 42 C210 57 255 89 266 111 C195 149 -165 166 -240 105 C-148 106 -10 65 150 42';
const BAND='M-83 0 C-26 18 54 3 116 -34 L128 1 C61 40 -12 51 -99 23';
// Blade split at y=-30. The needle stitches the same joint that breaks at the end.
const TOP='M0 -335 L-54 -205 L-40 -53 L-5 -26 L18 -49 L39 -31 L54 -205 Z';
const BOTTOM='M-40 -53 L-5 -26 L18 -49 L39 -31 L27 102 L56 160 L0 204 L-56 160 L-27 102 Z';
const GUARD='M-145 152 C-93 188 -48 169 0 173 C48 169 93 188 145 152 C116 205 65 208 30 202 L24 284 L0 312 L-24 284 L-30 202 C-65 208 -116 205 -145 152';
function hat(t,x,y,scale,rotation=0){
 const draw=mix(.17,1,E(t,0,1.0));
 let s=line(HAT,draw,PAPER,3.8)+line(BAND,E(t,.6,1.35),RED,3.4);
 return group(s,`translate(${x} ${y}) rotate(${rotation}) scale(${scale})`);
}
function sword(t,x,y,scale,rotation,injury){
 const birth=E(t,.65,2.1),heal=E(t,1.3,2.5),active=E(t,3.15,3.65);
 const separated=(1-heal)*58+injury*38;
 let s='';
 const fill=E(t,3.05,4.75)*(1-E(t,5.1,5.75))*.26;
 if(fill>0)s+=`<path d="${TOP}" fill="${RED}" opacity="${fill}"/>`;
 s+=group(line(TOP,birth,PAPER,3.7),`translate(${separated*.55} ${-separated}) rotate(${-injury*7} 0 -31)`);
 s+=line(BOTTOM,birth,PAPER,3.7)+line(GUARD,E(t,1.1,2.2),PAPER,3.7);
 s+=line('M0 -310 L0 -87',E(t,1.4,2.3),RED,3.0,.85);
 // Three stitches cross the join, then pull out after the impact.
 const stitch=appear(t,1.65,2.55,10.27,10.48);
 for(let i=0;i<3;i++)s+=line(`M${-29+i*21} -68 L${-16+i*21} -17`,stitch,RED,3.3);
 return group(s,`translate(${x} ${y}) rotate(${rotation-active*2}) scale(${scale})`);
}
function actors(t){
 const rise=E(t,5.56,6.42),relax=E(t,8.25,9.3),swell=Math.sin(E(t,2.8,5.55)*Math.PI);
 const landing=window.C.fifth.landing,impact=E(t,landing,landing+.095);
 const ring=appear(t,2.9,3.5,5.3,5.7);
 const response=E(t,7.1,7.75)*(1-E(t,8.25,8.75));
 const hx=mix(350,315,rise)+relax*5,hy=790+rise*24-relax*10;
 const sx=1440+rise*62+relax*193-response*50,sy=790-rise*185+relax*110;
 const rot=mix(-31,-4,E(t,.6,2.6))+rise*4+response*-7+impact*5;
 const recoil=t>=landing?Math.sin((t-landing)*62)*Math.exp(-(t-landing)*17)*18:0;
 const hatRotation=-3+rise*6-response*3-impact*5;
 const hr=hatRotation*Math.PI/180,br=(rot-E(t,3.15,3.65)*2)*Math.PI/180;
 const bladeScale=1.02+rise*.08-relax*.07;
 const brim=[hx+1.10*(266*Math.cos(hr)-111*Math.sin(hr)),hy+1.10*(266*Math.sin(hr)+111*Math.cos(hr))];
 const joint=[sx+recoil+bladeScale*(-40*Math.cos(br)+53*Math.sin(br)),sy+bladeScale*(-40*Math.sin(br)-53*Math.cos(br))];
 let s=hat(t,hx,hy,1.10,hatRotation);
 // A single connecting thread travels from the brim, through the needle, to the wound.
 const tension=E(t,4.8,5.68)*(1-relax);
 const slack=mix(840,620,tension)+relax*70-impact*115;
 const needleX=mix(820,1010,tension)-relax*130,needleY=slack-34;
 let thread=`M${brim[0]} ${brim[1]} C${hx+348} ${hy+62} ${needleX-155} ${needleY+40} ${needleX-63} ${needleY+10} C${needleX+12} ${needleY-2} ${needleX+192} ${needleY+70} ${joint[0]} ${joint[1]}`;
 s+=line(thread,E(t,.75,2.35),RED,3.6);
 // Needle, with a visible eye; its tip follows the repair direction.
 const needleOpacity=appear(t,.8,1.3,10.3,10.62);
 s+=group(line('M-68 21 Q-85 10 -68 -1 L112 -48 L-60 20 Q-68 23 -68 21 M-63 10 Q-70 3 -61 1 L-32 -5 Q-24 2 -35 3 Z',1,PAPER,3.1),`translate(${needleX} ${needleY})`,needleOpacity);
 if(ring>0){
  // The enclosing stroke is attached to the existing bond and wraps the sword once.
  s+=line(`M${sx-48} ${sy-53} C${sx-205} ${sy-160} ${sx-245} ${sy+210} ${sx-58} ${sy+239} C${sx+178} ${sy+267} ${sx+205} ${sy-102} ${sx+48} ${sy-95}`,ring,RED,3.4,ring);
 }
 s+=sword(t,sx+recoil,sy,bladeScale,rot,impact);
 if(impact>0){
  // Both loose ends remain attached to their respective objects; no decorative slash.
  s+=line(`M${joint[0]} ${joint[1]} Q${joint[0]-119} ${joint[1]-90} ${joint[0]-102} ${joint[1]-146}`,impact,RED,3.6);
  s+=line(`M${joint[0]+18} ${joint[1]-76} Q${joint[0]-9} ${joint[1]-134} ${joint[0]+36} ${joint[1]-160}`,impact,ROSE,3.2);
 }
 return s;
}
function lyrics(t){
 const C=window.C;let s='';
 const a=1-E(t,C.first.exit_start,C.first.exit_end);
 if(a>0){
  let z=hand('The magical potion of',180,85,1.13,E(t,.02,1.62));
  const p=E(t,1.3,2.2),join=(1-p)*26;
  z+=group(display('reanimation',440,424,230,PAPER),`translate(0 ${join})`,p);
  // The final letter extends into the descending repair path.
  z+=line('M1423 411 C1580 443 1590 630 1438 739',E(t,1.95,2.6),PAPER,3.2);
  s+=group(z,`translate(${-45*(1-a)} ${-28*(1-a)})`,a);
 }
 const b=appear(t,C.second.start,C.second.start+.18,C.second.exit_start,C.second.exit_end);
 if(b>0){
  let z=hand('Bittersweet',195,77+155*(1-E(t,2.75,3.35)),1.17,E(t,2.55,3.25));
  z+=hand('cranberry flavored',860,195,.83,E(t,3.03,3.95));
  const p=E(t,4,4.7),growth=1+.08*E(t,4.35,5.15);
  z+=group(display('euphoria',650,421,242,ROSE),`translate(1120 350) scale(${growth}) translate(-1120 -350)`,p);
  s+=group(z,`translate(0 ${-60*(1-b)})`,b);
 }
 const c=appear(t,C.third.start,C.third.start+.13,C.third.exit_start,C.third.exit_end);
 if(c>0){
  const p=clamp((t-C.third.start)/.52),spring=1-Math.exp(-7*p)*Math.cos(11*p),dy=(1-spring)*215;
  let z=display('Rise',150,437+dy,370,PAPER,1,`transform="rotate(-6 350 350)"`);
  if(p<.7)z+=display('Rise',150,437+dy+28*(1-p),370,RED,(1-p)*.12);
  z+=hand('from bed',790,230,1.0,E(t,C.third.from_bed,6.85));
  z+=group(display('my darling',630,520,181,ROSE),`translate(${(1-E(t,C.third.darling,7.45))*76} 0)`,E(t,C.third.darling,7.45));
  s+=group(z,`translate(0 ${-38*(1-c)})`,c);
 }
 const d=appear(t,C.fourth.start,8.8,C.fifth.exit_start,C.fifth.exit_end);
 if(d>0){
  let z=hand('So I can',215,72,1.18,E(t,8.5,9.04));
  const see=E(t,C.fourth.see,9.28)*(1-E(t,C.fourth.exit_start+.0667,C.fourth.exit_end));
  z+=display('see',740,454,358,PAPER,see);
  z+=hand('you again',1190,334,.79,E(t,9.15,9.64));
  if(t+1e-8>=C.fifth.landing){
   const dt=t-C.fifth.landing,settle=Math.exp(-dt*25),hit=Math.sin(dt*60)*Math.exp(-dt*21)*8;
   if(dt<1/30)z+=display('kill',560,490,450,ROSE,.45,'transform="translate(40 -18) skewX(-8)"');
   z+=display('kill',540+hit,490+settle*14,450,RED,1,`transform="rotate(${-4+settle*2} 950 390)"`);
  }
  s+=group(z,'',d);
 }
 return s;
}
window.render=t=>{
 const C=window.C;
 const flash=t>=C.fifth.flash&&t<C.fifth.landing-1e-8;
 const impact=t>=C.fifth.landing?Math.sin((t-C.fifth.landing)*60)*Math.exp(-(t-C.fifth.landing)*18)*7:0;
 const focus=E(t,5.5,6.5)*(1-E(t,8.25,9.35));
 const cam=`translate(${impact} ${-focus*18+impact*.35}) translate(960 610) scale(${1+.025*focus}) translate(-960 -610)`;
 let s=`<defs><radialGradient id="ground"><stop stop-color="#1b191b"/><stop offset="1" stop-color="${INK}"/></radialGradient></defs><rect width="1920" height="1080" fill="url(#ground)"/>`;
 s+=group(actors(t)+lyrics(t),cam);
 if(flash)s+=`<rect width="1920" height="1080" fill="${RED}" opacity="${t<C.fifth.flash+1/30?.78:.43}"/>`;
 document.getElementById('stage').innerHTML=s;
};
