(function(){
  var WA='https://wa.me/971585414999?text=';
  var d=document,b=d.body;
  function $(s,c){return (c||d).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}
  function aed(n){return 'AED '+Math.round(n).toLocaleString('en-US')}
  function openWA(t){window.open(WA+encodeURIComponent(t),'_blank','noopener')}

  /* menu */
  var burger=$('.burger');
  if(burger){burger.addEventListener('click',function(){var o=b.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o)});
    $$('.nav a').forEach(function(a){a.addEventListener('click',function(){b.classList.remove('menu-open');burger.setAttribute('aria-expanded','false')})});}

  /* transparent header on home */
  var hdr=$('.hdr.home');
  if(hdr){var f=function(){hdr.classList.toggle('solid',window.scrollY>window.innerHeight*0.55)};f();window.addEventListener('scroll',f,{passive:true});}

  /* hero video */
  var v=$('.hero video');
  if(v){v.muted=true;var r=function(){try{v.playbackRate=1.5}catch(e){}};r();v.addEventListener('loadedmetadata',r);v.addEventListener('play',r);
    var p=v.play();if(p&&p.catch)p.catch(function(){});}

  /* in-view videos: play only while visible */
  var iv=$$('video[data-inview]');
  if(iv.length){iv.forEach(function(x){x.muted=true});
    if('IntersectionObserver' in window&&!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)){
      var vo=new IntersectionObserver(function(es){es.forEach(function(e){var x=e.target;if(e.isIntersecting){var q=x.play();if(q&&q.catch)q.catch(function(){})}else x.pause()})},{threshold:0.25});
      iv.forEach(function(x){vo.observe(x)});}else{iv.forEach(function(x){x.controls=true})}}

  /* reveal */
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    $$('.reveal').forEach(function(el){io.observe(el)});}else{$$('.reveal').forEach(function(el){el.classList.add('in')})}

  /* enquiry forms -> WhatsApp */
  $$('form[data-wa]').forEach(function(fm){
    fm.addEventListener('submit',function(e){e.preventDefault();
      var lines=[fm.getAttribute('data-wa')];
      $$('.field',fm).forEach(function(fl){var l=$('label',fl),i=$('input,select,textarea',fl);if(!l||!i)return;var val=(i.value||'').trim();if(val)lines.push(l.textContent.replace(/\s*\*$/,'')+': '+val)});
      openWA(lines.join('\n'));
    });
  });

  /* listings */
  var grid=$('#listings-grid');
  if(grid){
    var cards=$$('.lst',grid),fb=$('#f-beds'),ff=$('#f-frond'),fs=$('#f-sort'),cnt=$('#f-count');
    var sel=[],bar=$('.shortbar'),barN=$('#bar-n'),barSend=$('#bar-send');
    function apply(){var n=0,list=cards.slice();
      list.sort(function(a,c){var x=+a.dataset.price,y=+c.dataset.price;return fs.value==='desc'?y-x:x-y});
      list.forEach(function(c){grid.appendChild(c);var ok=(fb.value==='all'||c.dataset.beds===fb.value)&&(ff.value==='all'||c.dataset.frond===ff.value);c.hidden=!ok;if(ok)n++});
      cnt.textContent=n+(n===1?' villa':' villas');}
    try{var q=new URLSearchParams(location.search);if(q.get('frond')&&$('option[value="'+q.get('frond')+'"]',ff))ff.value=q.get('frond');if(q.get('beds')&&$('option[value="'+q.get('beds')+'"]',fb))fb.value=q.get('beds');}catch(e){}
    [fb,ff,fs].forEach(function(x){x.addEventListener('change',apply)});apply();
    function upd(){barN.textContent=sel.length+(sel.length===1?' villa selected':' villas selected');bar.classList.toggle('show',sel.length>0);b.classList.toggle('has-bar',sel.length>0)}
    cards.forEach(function(c){
      $('.add',c).addEventListener('click',function(){var id=c.dataset.id,i=sel.indexOf(id),btn=this;
        if(i<0){sel.push(id);btn.setAttribute('aria-pressed','true');btn.textContent='Shortlisted ✓'}else{sel.splice(i,1);btn.setAttribute('aria-pressed','false');btn.textContent='Add to shortlist'}upd()});
      $('.ask',c).addEventListener('click',function(e){e.preventDefault();openWA('Hello Mark, please confirm availability, price and remaining developer payments for this Palm Jebel Ali villa:\n'+c.dataset.summary)});
    });
    barSend.addEventListener('click',function(){var t=['Hello Mark, please confirm availability, price and remaining developer payments for my Palm Jebel Ali shortlist:'];
      sel.forEach(function(id,k){var c=$('.lst[data-id="'+id+'"]',grid);t.push((k+1)+'. '+c.dataset.summary)});openWA(t.join('\n'))});
  }

  /* sortable tables */
  $$('table.sortable').forEach(function(t){
    $$('th',t).forEach(function(th,i){th.addEventListener('click',function(){
      var tb=t.tBodies[0],rows=$$('tr',tb),asc=th.dataset.dir!=='asc';
      $$('th',t).forEach(function(h){delete h.dataset.dir});th.dataset.dir=asc?'asc':'desc';
      rows.sort(function(a,b){var x=a.cells[i].dataset.v||a.cells[i].textContent,y=b.cells[i].dataset.v||b.cells[i].textContent;
        var nx=parseFloat(x),ny=parseFloat(y);var r=(!isNaN(nx)&&!isNaN(ny))?nx-ny:String(x).localeCompare(String(y));return asc?r:-r});
      rows.forEach(function(r){tb.appendChild(r)});
    })});
  });

  /* cost estimator */
  var calc=$('#calc');
  if(calc){var g=function(id){return parseFloat(($('#'+id).value||'').replace(/,/g,''))||0};
    function run(){var price=g('c-price'),dld=price*(+$('#c-dld').value)/100,brk=price*g('c-brk')/100,vat=brk*0.05,title=price?520:0,oth=g('c-oth'),tot=price+dld+brk+vat+title+oth;
      $('#o-price').textContent=aed(price);$('#o-dld').textContent=aed(dld);$('#o-brk').textContent=aed(brk);$('#o-vat').textContent=aed(vat);$('#o-title').textContent=aed(title);$('#o-oth').textContent=aed(oth);$('#o-tot').textContent=price?aed(tot):'Enter a price';
      var oc=g('b-price'),pc=+$('#b-paid').value;$('#o-paid').textContent=aed(oc*pc/100);$('#o-bal').textContent=oc?aed(oc*(100-pc)/100):'Enter contract price';}
    $$('input,select',calc).forEach(function(x){x.addEventListener('input',run);x.addEventListener('change',run)});run();}

  /* position compare */
  var cmp=$('#cmp');
  if(cmp){var keys=[['frond','Frond'],['ori','Orientation'],['pos','Position along frond'],['out','Outlook'],['nb','Neighbour relationship'],['paid','Developer amount paid']];
    var body=$('#cmp-body'),todo=$('#cmp-todo'),send=$('#cmp-send');
    function val(o,k){return $('[name="'+o+'-'+k+'"]',cmp).value}
    function run(){var h='',miss=[];keys.forEach(function(k){var a=val('o1',k[0]),c=val('o2',k[0]);h+='<tr><td>'+k[1]+'</td><td class="'+(a==='Not verified'?'tbv':'')+'">'+a+'</td><td class="'+(c==='Not verified'?'tbv':'')+'">'+c+'</td></tr>';if(a==='Not verified'||c==='Not verified')miss.push(k[1])});
      body.innerHTML=h;todo.textContent=miss.length?'Still to verify: '+miss.join(', ')+'.':'All position fields entered. Asking price, exact plot, outstanding balance and instalment dates still need an individual review.';}
    $$('select,input',cmp).forEach(function(x){x.addEventListener('change',run);x.addEventListener('input',run)});run();
    send.addEventListener('click',function(){var t=['Hello Mark, please help me compare these Palm Jebel Ali villa positions.','My priority: '+$('#cmp-pri').value,'These are my inputs, to be checked against the villa documents.'];
      ['o1','o2'].forEach(function(o,i){t.push('','Option '+(i+1)+': '+($('[name="'+o+'-ref"]',cmp).value||'Reference to discuss'));keys.forEach(function(k){t.push(k[1]+': '+val(o,k[0]))})});
      t.push('','Please also compare layout, asking price, outstanding developer balance, instalment dates and transfer requirements.');openWA(t.join('\n'))});
  }
})();
