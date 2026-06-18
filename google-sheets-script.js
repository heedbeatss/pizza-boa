var SHEET_ID = '1EwtGeTtkl0WcKdl_2UZrZhLAU55xfx0hLAEkn1kN_2M';
var CARDAPIO_SHEET = 'Cardapio';
var PEDIDOS_SHEET = 'Pedidos';
var CONFIG_SHEET = 'Config';

function inicializar() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var cardapio = ss.getSheetByName(CARDAPIO_SHEET);
  if (!cardapio) {
    cardapio = ss.insertSheet(CARDAPIO_SHEET);
    cardapio.appendRow(['categoriaId','categoriaNome','categoriaIcone','itemId','itemNome','itemDescricao','tamanho','fatias','preco']);
  }
  var pedidos = ss.getSheetByName(PEDIDOS_SHEET);
  if (!pedidos) {
    pedidos = ss.insertSheet(PEDIDOS_SHEET);
    pedidos.appendRow(['pedidoId','data/horario','nome','telefone','rua+numero','bairro','cep','complemento','referencia','retirada','pagamento','troco','obs','itens','subtotal','entrega','totalFinal','status']);
  }
  var config = ss.getSheetByName(CONFIG_SHEET);
  if (!config) {
    config = ss.insertSheet(CONFIG_SHEET);
    config.appendRow(['chave','valor']);
    config.appendRow(['horarioInicio','18']);
    config.appendRow(['horarioFim','1']);
    config.appendRow(['taxaMaxima','15']);
    config.appendRow(['pedidoGratisMinimo','100']);
    config.appendRow(['whatsapp','19984356289']);
  }
  SpreadsheetApp.getUi().alert('Planilha inicializada!');
}

function doGet(e) {
  var action = e.parameter.action;
  if (action === 'cardapio') return getCardapio();
  if (action === 'pedidos') return getPedidos(e);
  if (action === 'pedido') return getPedido(e);
  if (action === 'config') return getConfig();
  return ContentService.createTextOutput(JSON.stringify({error:'Acao invalida'})).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var raw = '';
  try { raw = e.postData ? e.postData.contents : ''; } catch(ex) {}
  if (!raw) {
    return ContentService.createTextOutput(JSON.stringify({error:'body vazio', debug: 'no postData'})).setMimeType(ContentService.MimeType.JSON);
  }
  var data;
  try { data = JSON.parse(raw); } catch(err) {
    // Tenta parsear como URL-encoded (form submit): data={...}
    try {
      var params = {};
      var parts = raw.split('&');
      for (var p = 0; p < parts.length; p++) {
        var kv = parts[p].split('=');
        params[decodeURIComponent(kv[0])] = decodeURIComponent(kv.slice(1).join('='));
      }
      if (params.data) {
        data = JSON.parse(params.data);
      } else {
        data = params;
      }
    } catch(err2) {
      try { data = JSON.parse(decodeURIComponent(raw)); } catch(err3) {
        return ContentService.createTextOutput(JSON.stringify({error:'JSON invalido', raw: raw.substring(0,200)})).setMimeType(ContentService.MimeType.JSON);
      }
    }
  }
  var action = data.action;
  if (action === 'novoPedido') return criarPedido(data.data || data);
  if (action === 'atualizarStatus') return atualizarStatus(data.data || data);
  return ContentService.createTextOutput(JSON.stringify({error:'Acao invalida', action:action})).setMimeType(ContentService.MimeType.JSON);
}

function getCardapio() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(CARDAPIO_SHEET);
  var data = sheet.getDataRange().getValues();
  var categoriasMap = {};
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var catId = String(row[0]);
    if (!catId || catId === '') continue;
    if (!categoriasMap[catId]) {
      categoriasMap[catId] = {id:catId, nome:row[1], icone:row[2], itens:[]};
    }
    var itemId = String(row[3]);
    var existing = null;
    for (var k = 0; k < categoriasMap[catId].itens.length; k++) {
      if (categoriasMap[catId].itens[k].id === itemId) { existing = categoriasMap[catId].itens[k]; break; }
    }
    if (!existing) {
      existing = {id:itemId, nome:row[4], descricao:row[5], tamanhos:[]};
      categoriasMap[catId].itens.push(existing);
    }
    existing.tamanhos.push({nome:row[6], fatias:row[7]?parseInt(row[7]):null, preco:parseFloat(row[8])});
  }
  var categorias = [];
  for (var key in categoriasMap) categorias.push(categoriasMap[key]);
  return ContentService.createTextOutput(JSON.stringify({categorias:categorias})).setMimeType(ContentService.MimeType.JSON);
}

function getPedidos(e) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(PEDIDOS_SHEET);
  var data = sheet.getDataRange().getValues();
  var pedidos = [];
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    if (!row[0]) continue;
    pedidos.push(rowToPedido(row));
  }
  pedidos.sort(function(a,b){return b.id-a.id;});
  return ContentService.createTextOutput(JSON.stringify({total:pedidos.length,pedidos:pedidos})).setMimeType(ContentService.MimeType.JSON);
}

function getPedido(e) {
  var id = parseInt(e.parameter.id);
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(PEDIDOS_SHEET);
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (data[i][0] === id) return ContentService.createTextOutput(JSON.stringify(rowToPedido(data[i]))).setMimeType(ContentService.MimeType.JSON);
  }
  return ContentService.createTextOutput(JSON.stringify({error:'Pedido nao encontrado'})).setMimeType(ContentService.MimeType.JSON);
}

function rowToPedido(row) {
  var itensRaw = row[13];
  var itens = [];
  try { itens = typeof itensRaw==='string'?JSON.parse(itensRaw):(Array.isArray(itensRaw)?itensRaw:[]); } catch(e){itens=[];}
  return {
    id:row[0], data:row[1] instanceof Date?row[1].toISOString():row[1], nome:row[2], telefone:String(row[3]),
    endereco:{rua:row[4]||'',bairro:row[5]||'',cep:row[6]||'',complemento:row[7]||'',referencia:row[8]||'',retirada:row[9]==='true'||row[9]===true||row[9]==='RETIRADA'},
    pagamento:row[10], troco:row[11], obs:row[12], itens:itens,
    subtotal:parseFloat(row[14])||0, entrega:parseFloat(row[15])||0, totalFinal:parseFloat(row[16])||0, status:row[17]
  };
}

function getConfig() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(CONFIG_SHEET);
  var data = sheet.getDataRange().getValues();
  var config = {};
  for (var i = 1; i < data.length; i++) config[data[i][0]] = data[i][1];
  return ContentService.createTextOutput(JSON.stringify(config)).setMimeType(ContentService.MimeType.JSON);
}

function criarPedido(data) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(PEDIDOS_SHEET);
  var dataRows = sheet.getDataRange().getValues();
  var maxId = 0;
  for (var i = 1; i < dataRows.length; i++) { var v=parseInt(dataRows[i][0]); if(v&&v>maxId)maxId=v; }
  var novoId = maxId + 1;
  var itens = data.itens||[];
  var subtotal = 0;
  for (var i=0;i<itens.length;i++) subtotal+=(itens[i].preco||0)*(itens[i].qty||1);
  var entrega = parseFloat(data.entrega)||0;
  var totalFinal = subtotal+entrega;
  var end = data.endereco||{};
  var isRetirada = end.retirada === true || end.retirada === 'true';
  var ruaNumero = (end.rua||'') + (end.numero ? ', ' + end.numero : '');
  sheet.appendRow([
    novoId,
    new Date(),
    data.nome||'',
    data.telefone||'',
    ruaNumero,
    end.bairro||'',
    end.cep||'',
    end.complemento||'',
    end.referencia||'',
    isRetirada ? 'RETIRADA' : 'ENTREGA',
    data.pagamento||'dinheiro',
    data.troco||'',
    data.obs||'',
    JSON.stringify(itens),
    subtotal,
    entrega,
    totalFinal,
    'recebido'
  ]);
  return ContentService.createTextOutput(JSON.stringify({success:true,pedidoId:novoId})).setMimeType(ContentService.MimeType.JSON);
}

var STATUS_VALIDOS = ['recebido','confirmado','em_preparo','no_forno','saiu_entrega','retirou','entregue','cancelado'];

function atualizarStatus(data) {
  var id = parseInt(data.pedidoId);
  var status = data.status;
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(PEDIDOS_SHEET);
  var dataRows = sheet.getDataRange().getValues();
  for (var i = 1; i < dataRows.length; i++) {
    if (parseInt(dataRows[i][0])===id) {
      sheet.getRange(i+1,18).setValue(status);
      return ContentService.createTextOutput(JSON.stringify({success:true,message:'Status atualizado para '+status})).setMimeType(ContentService.MimeType.JSON);
    }
  }
  return ContentService.createTextOutput(JSON.stringify({error:'Pedido nao encontrado'})).setMimeType(ContentService.MimeType.JSON);
}

function popularCardapio() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(CARDAPIO_SHEET);
  if (!sheet) { sheet = ss.insertSheet(CARDAPIO_SHEET); }
  sheet.clear();
  sheet.appendRow(['categoriaId','categoriaNome','categoriaIcone','itemId','itemNome','itemDescricao','tamanho','fatias','preco']);
  var d = [
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mussarela','Mussarela','Molho, mussarela e orégano','Broto',4,25],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mussarela','Mussarela','Molho, mussarela e orégano','Media',6,35],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mussarela','Mussarela','Molho, mussarela e orégano','Grande',8,45],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mussarela','Mussarela','Molho, mussarela e orégano','Familia',12,60],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','calabresa','Calabresa','Calabresa, cebola e azeitona','Broto',4,28],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','calabresa','Calabresa','Calabresa, cebola e azeitona','Media',6,38],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','calabresa','Calabresa','Calabresa, cebola e azeitona','Grande',8,48],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','calabresa','Calabresa','Calabresa, cebola e azeitona','Familia',12,60],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-catupiry','Frango c/ Catupiry','Frango desfiado e catupiry','Broto',4,30],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-catupiry','Frango c/ Catupiry','Frango desfiado e catupiry','Media',6,40],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-catupiry','Frango c/ Catupiry','Frango desfiado e catupiry','Grande',8,52],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-catupiry','Frango c/ Catupiry','Frango desfiado e catupiry','Familia',12,70],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','portuguesa','Portuguesa','Presunto, ovo, cebola e azeitona','Broto',4,30],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','portuguesa','Portuguesa','Presunto, ovo, cebola e azeitona','Media',6,42],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','portuguesa','Portuguesa','Presunto, ovo, cebola e azeitona','Grande',8,54],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','portuguesa','Portuguesa','Presunto, ovo, cebola e azeitona','Familia',12,70],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon','Bacon','Bacon e mussarela','Broto',4,30],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon','Bacon','Bacon e mussarela','Media',6,40],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon','Bacon','Bacon e mussarela','Grande',8,52],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon','Bacon','Bacon e mussarela','Familia',12,70],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','margherita','Margherita','Mussarela, tomate e manjericão','Broto',4,28],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','margherita','Margherita','Mussarela, tomate e manjericão','Media',6,38],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','margherita','Margherita','Mussarela, tomate e manjericão','Grande',8,48],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','margherita','Margherita','Mussarela, tomate e manjericão','Familia',12,60],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','napolitana','Napolitana','Mussarela, tomate, parmesão e orégano','Broto',4,30],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','napolitana','Napolitana','Mussarela, tomate, parmesão e orégano','Media',6,40],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','napolitana','Napolitana','Mussarela, tomate, parmesão e orégano','Grande',8,52],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','napolitana','Napolitana','Mussarela, tomate, parmesão e orégano','Familia',12,70],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','peperoni','Peperoni','Mussarela, peperoni e orégano','Broto',4,32],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','peperoni','Peperoni','Mussarela, peperoni e orégano','Media',6,44],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','peperoni','Peperoni','Mussarela, peperoni e orégano','Grande',8,56],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','peperoni','Peperoni','Mussarela, peperoni e orégano','Familia',12,75],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','4-queijos','4 Queijos','Mussarela, provolone, parmesão e gorgonzola','Broto',4,32],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','4-queijos','4 Queijos','Mussarela, provolone, parmesão e gorgonzola','Media',6,44],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','4-queijos','4 Queijos','Mussarela, provolone, parmesão e gorgonzola','Grande',8,58],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','4-queijos','4 Queijos','Mussarela, provolone, parmesão e gorgonzola','Familia',12,75],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','3-queijos','3 Queijos','Mussarela, catupiry e parmesão','Broto',4,30],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','3-queijos','3 Queijos','Mussarela, catupiry e parmesão','Media',6,40],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','3-queijos','3 Queijos','Mussarela, catupiry e parmesão','Grande',8,52],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','3-queijos','3 Queijos','Mussarela, catupiry e parmesão','Familia',12,70],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','catupiry','Catupiry','Mussarela e catupiry original','Broto',4,28],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','catupiry','Catupiry','Mussarela e catupiry original','Media',6,38],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','catupiry','Catupiry','Mussarela e catupiry original','Grande',8,48],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','catupiry','Catupiry','Mussarela e catupiry original','Familia',12,60],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','atum','Atum','Atum, cebola e mussarela','Broto',4,32],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','atum','Atum','Atum, cebola e mussarela','Media',6,44],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','atum','Atum','Atum, cebola e mussarela','Grande',8,56],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','atum','Atum','Atum, cebola e mussarela','Familia',12,75],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mista','Mista','Presunto, mussarela e orégano','Broto',4,26],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mista','Mista','Presunto, mussarela e orégano','Media',6,36],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mista','Mista','Presunto, mussarela e orégano','Grande',8,46],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','mista','Mista','Presunto, mussarela e orégano','Familia',12,60],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vienna','Vienna','Linguiça calabresa e mussarela','Broto',4,30],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vienna','Vienna','Linguiça calabresa e mussarela','Media',6,40],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vienna','Vienna','Linguiça calabresa e mussarela','Grande',8,52],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vienna','Vienna','Linguiça calabresa e mussarela','Familia',12,70],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon-cheddar','Bacon c/ Cheddar','Bacon e cheddar cremoso','Broto',4,32],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon-cheddar','Bacon c/ Cheddar','Bacon e cheddar cremoso','Media',6,44],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon-cheddar','Bacon c/ Cheddar','Bacon e cheddar cremoso','Grande',8,56],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','bacon-cheddar','Bacon c/ Cheddar','Bacon e cheddar cremoso','Familia',12,75],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-cream-cheese','Frango c/ Cream Cheese','Frango desfiado e cream cheese','Broto',4,32],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-cream-cheese','Frango c/ Cream Cheese','Frango desfiado e cream cheese','Media',6,44],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-cream-cheese','Frango c/ Cream Cheese','Frango desfiado e cream cheese','Grande',8,56],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','frango-cream-cheese','Frango c/ Cream Cheese','Frango desfiado e cream cheese','Familia',12,75],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','escalopes','Escalopes de Carne','Mussarela, carne bovina e cebola','Broto',4,34],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','escalopes','Escalopes de Carne','Mussarela, carne bovina e cebola','Media',6,46],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','escalopes','Escalopes de Carne','Mussarela, carne bovina e cebola','Grande',8,60],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','escalopes','Escalopes de Carne','Mussarela, carne bovina e cebola','Familia',12,80],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','camarao','Camarão','Camarão, catupiry e mussarela','Broto',4,38],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','camarao','Camarão','Camarão, catupiry e mussarela','Media',6,52],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','camarao','Camarão','Camarão, catupiry e mussarela','Grande',8,68],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','camarao','Camarão','Camarão, catupiry e mussarela','Familia',12,90],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vegetariana','Vegetariana','Brócolis, champignon, cebola e mussarela','Broto',4,30],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vegetariana','Vegetariana','Brócolis, champignon, cebola e mussarela','Media',6,42],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vegetariana','Vegetariana','Brócolis, champignon, cebola e mussarela','Grande',8,54],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','vegetariana','Vegetariana','Brócolis, champignon, cebola e mussarela','Familia',12,70],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','rúcula','Rúcula com Tomate Seco','Rúcula, tomate seco e mussarela de búfala','Broto',4,34],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','rúcula','Rúcula com Tomate Seco','Rúcula, tomate seco e mussarela de búfala','Media',6,46],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','rúcula','Rúcula com Tomate Seco','Rúcula, tomate seco e mussarela de búfala','Grande',8,60],
    ['pizzas-salgadas','Pizzas Salgadas','🍕','rúcula','Rúcula com Tomate Seco','Rúcula, tomate seco e mussarela de búfala','Familia',12,80],
    ['pizzas-especiais','Especiais da Casa','⭐','pizza-supreme','Supreme','Peperoni, calabresa, cebola, pimentão e azeitona','Broto',4,38],
    ['pizzas-especiais','Especiais da Casa','⭐','pizza-supreme','Supreme','Peperoni, calabresa, cebola, pimentão e azeitona','Media',6,52],
    ['pizzas-especiais','Especiais da Casa','⭐','pizza-supreme','Supreme','Peperoni, calabresa, cebola, pimentão e azeitona','Grande',8,68],
    ['pizzas-especiais','Especiais da Casa','⭐','pizza-supreme','Supreme','Peperoni, calabresa, cebola, pimentão e azeitona','Familia',12,90],
    ['pizzas-especiais','Especiais da Casa','⭐','costela','Costela no Bafo','Costela desfiada, barbecue e cebola caramelizada','Broto',4,40],
    ['pizzas-especiais','Especiais da Casa','⭐','costela','Costela no Bafo','Costela desfiada, barbecue e cebola caramelizada','Media',6,55],
    ['pizzas-especiais','Especiais da Casa','⭐','costela','Costela no Bafo','Costela desfiada, barbecue e cebola caramelizada','Grande',8,72],
    ['pizzas-especiais','Especiais da Casa','⭐','costela','Costela no Bafo','Costela desfiada, barbecue e cebola caramelizada','Familia',12,95],
    ['pizzas-especiais','Especiais da Casa','⭐','bacon-explosao','Bacon Explosão','Bacon, cheddar, parmesão e orégano','Broto',4,38],
    ['pizzas-especiais','Especiais da Casa','⭐','bacon-explosao','Bacon Explosão','Bacon, cheddar, parmesão e orégano','Media',6,52],
    ['pizzas-especiais','Especiais da Casa','⭐','bacon-explosao','Bacon Explosão','Bacon, cheddar, parmesão e orégano','Grande',8,68],
    ['pizzas-especiais','Especiais da Casa','⭐','bacon-explosao','Bacon Explosão','Bacon, cheddar, parmesão e orégano','Familia',12,90],
    ['pizzas-especiais','Especiais da Casa','⭐','frango-real','Frango Real','Frango, catupiry, milho e batata palha','Broto',4,36],
    ['pizzas-especiais','Especiais da Casa','⭐','frango-real','Frango Real','Frango, catupiry, milho e batata palha','Media',6,50],
    ['pizzas-especiais','Especiais da Casa','⭐','frango-real','Frango Real','Frango, catupiry, milho e batata palha','Grande',8,65],
    ['pizzas-especiais','Especiais da Casa','⭐','frango-real','Frango Real','Frango, catupiry, milho e batata palha','Familia',12,85],
    ['pizzas-especiais','Especiais da Casa','⭐','carne-seca','Carne Seca c/ Catupiry','Carne seca desfiada e catupiry','Broto',4,40],
    ['pizzas-especiais','Especiais da Casa','⭐','carne-seca','Carne Seca c/ Catupiry','Carne seca desfiada e catupiry','Media',6,55],
    ['pizzas-especiais','Especiais da Casa','⭐','carne-seca','Carne Seca c/ Catupiry','Carne seca desfiada e catupiry','Grande',8,72],
    ['pizzas-especiais','Especiais da Casa','⭐','carne-seca','Carne Seca c/ Catupiry','Carne seca desfiada e catupiry','Familia',12,95],
    ['pizzas-especiais','Especiais da Casa','⭐','marguerita-especial','Marguerita Especial','Mussarela de búfala, tomate e manjericão fresco','Broto',4,38],
    ['pizzas-especiais','Especiais da Casa','⭐','marguerita-especial','Marguerita Especial','Mussarela de búfala, tomate e manjericão fresco','Media',6,52],
    ['pizzas-especiais','Especiais da Casa','⭐','marguerita-especial','Marguerita Especial','Mussarela de búfala, tomate e manjericão fresco','Grande',8,68],
    ['pizzas-especiais','Especiais da Casa','⭐','marguerita-especial','Marguerita Especial','Mussarela de búfala, tomate e manjericão fresco','Familia',12,90],
    ['pizzas-especiais','Especiais da Casa','⭐','lombo-canadense','Lombo Canadense','Lombo, cebola e mussarela','Broto',4,38],
    ['pizzas-especiais','Especiais da Casa','⭐','lombo-canadense','Lombo Canadense','Lombo, cebola e mussarela','Media',6,52],
    ['pizzas-especiais','Especiais da Casa','⭐','lombo-canadense','Lombo Canadense','Lombo, cebola e mussarela','Grande',8,68],
    ['pizzas-especiais','Especiais da Casa','⭐','lombo-canadense','Lombo Canadense','Lombo, cebola e mussarela','Familia',12,90],
    ['pizzas-especiais','Especiais da Casa','⭐','coração','Coração de Frango','Coração de frango, catupiry e cebola','Broto',4,35],
    ['pizzas-especiais','Especiais da Casa','⭐','coração','Coração de Frango','Coração de frango, catupiry e cebola','Media',6,48],
    ['pizzas-especiais','Especiais da Casa','⭐','coração','Coração de Frango','Coração de frango, catupiry e cebola','Grande',8,62],
    ['pizzas-especiais','Especiais da Casa','⭐','coração','Coração de Frango','Coração de frango, catupiry e cebola','Familia',12,80],
    ['pizzas-especiais','Especiais da Casa','⭐','gorgonzola','Gorgonzola com Nozes','Gorgonzola, mozzarella e nozes','Broto',4,40],
    ['pizzas-especiais','Especiais da Casa','⭐','gorgonzola','Gorgonzola com Nozes','Gorgonzola, mozzarella e nozes','Media',6,55],
    ['pizzas-especiais','Especiais da Casa','⭐','gorgonzola','Gorgonzola com Nozes','Gorgonzola, mozzarella e nozes','Grande',8,72],
    ['pizzas-especiais','Especiais da Casa','⭐','gorgonzola','Gorgonzola com Nozes','Gorgonzola, mozzarella e nozes','Familia',12,95],
    ['pizzas-especiais','Especiais da Casa','⭐','pepperoni-especial','Pepperoni Especial','Pepperoni artesanal e mozzarella premium','Broto',4,40],
    ['pizzas-especiais','Especiais da Casa','⭐','pepperoni-especial','Pepperoni Especial','Pepperoni artesanal e mozzarella premium','Media',6,55],
    ['pizzas-especiais','Especiais da Casa','⭐','pepperoni-especial','Pepperoni Especial','Pepperoni artesanal e mozzarella premium','Grande',8,72],
    ['pizzas-especiais','Especiais da Casa','⭐','pepperoni-especial','Pepperoni Especial','Pepperoni artesanal e mozzarella premium','Familia',12,95],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate','Chocolate','Chocolate ao leite e granulado','Broto',4,28],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate','Chocolate','Chocolate ao leite e granulado','Media',6,38],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate','Chocolate','Chocolate ao leite e granulado','Grande',8,48],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate','Chocolate','Chocolate ao leite e granulado','Familia',12,60],
    ['pizzas-doces','Pizzas Doces','🍫','prestigio','Prestígio','Chocolate, coco ralado e leite condensado','Broto',4,30],
    ['pizzas-doces','Pizzas Doces','🍫','prestigio','Prestígio','Chocolate, coco ralado e leite condensado','Media',6,40],
    ['pizzas-doces','Pizzas Doces','🍫','prestigio','Prestígio','Chocolate, coco ralado e leite condensado','Grande',8,52],
    ['pizzas-doces','Pizzas Doces','🍫','prestigio','Prestígio','Chocolate, coco ralado e leite condensado','Familia',12,70],
    ['pizzas-doces','Pizzas Doces','🍫','banana-canela','Banana c/ Canela','Banana, canela e leite condensado','Broto',4,25],
    ['pizzas-doces','Pizzas Doces','🍫','banana-canela','Banana c/ Canela','Banana, canela e leite condensado','Media',6,35],
    ['pizzas-doces','Pizzas Doces','🍫','banana-canela','Banana c/ Canela','Banana, canela e leite condensado','Grande',8,45],
    ['pizzas-doces','Pizzas Doces','🍫','banana-canela','Banana c/ Canela','Banana, canela e leite condensado','Familia',12,60],
    ['pizzas-doces','Pizzas Doces','🍫','romeu-julieta','Romeu e Julieta','Goiabada e queijo minas','Broto',4,28],
    ['pizzas-doces','Pizzas Doces','🍫','romeu-julieta','Romeu e Julieta','Goiabada e queijo minas','Media',6,38],
    ['pizzas-doces','Pizzas Doces','🍫','romeu-julieta','Romeu e Julieta','Goiabada e queijo minas','Grande',8,48],
    ['pizzas-doces','Pizzas Doces','🍫','romeu-julieta','Romeu e Julieta','Goiabada e queijo minas','Familia',12,60],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate-branco','Chocolate Branco','Chocolate branco e morango','Broto',4,32],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate-branco','Chocolate Branco','Chocolate branco e morango','Media',6,42],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate-branco','Chocolate Branco','Chocolate branco e morango','Grande',8,54],
    ['pizzas-doces','Pizzas Doces','🍫','chocolate-branco','Chocolate Branco','Chocolate branco e morango','Familia',12,70],
    ['pizzas-doces','Pizzas Doces','🍫','banana-nutella','Banana c/ Nutella','Banana e Nutella','Broto',4,35],
    ['pizzas-doces','Pizzas Doces','🍫','banana-nutella','Banana c/ Nutella','Banana e Nutella','Media',6,48],
    ['pizzas-doces','Pizzas Doces','🍫','banana-nutella','Banana c/ Nutella','Banana e Nutella','Grande',8,62],
    ['pizzas-doces','Pizzas Doces','🍫','banana-nutella','Banana c/ Nutella','Banana e Nutella','Familia',12,80],
    ['pizzas-doces','Pizzas Doces','🍫','nutella','Nutella','Nutella com morango','Broto',4,38],
    ['pizzas-doces','Pizzas Doces','🍫','nutella','Nutella','Nutella com morango','Media',6,50],
    ['pizzas-doces','Pizzas Doces','🍫','nutella','Nutella','Nutella com morango','Grande',8,65],
    ['pizzas-doces','Pizzas Doces','🍫','nutella','Nutella','Nutella com morango','Familia',12,85],
    ['pizzas-doces','Pizzas Doces','🍫','sorvete','Sorvete','Chocolate, sorvete e cobertura','Broto',4,35],
    ['pizzas-doces','Pizzas Doces','🍫','sorvete','Sorvete','Chocolate, sorvete e cobertura','Media',6,48],
    ['pizzas-doces','Pizzas Doces','🍫','sorvete','Sorvete','Chocolate, sorvete e cobertura','Grande',8,62],
    ['pizzas-doces','Pizzas Doces','🍫','sorvete','Sorvete','Chocolate, sorvete e cobertura','Familia',12,80],
    ['pizzas-doces','Pizzas Doces','🍫','churros','Churros','Doce de leite, canela e açúcar','Broto',4,30],
    ['pizzas-doces','Pizzas Doces','🍫','churros','Churros','Doce de leite, canela e açúcar','Media',6,42],
    ['pizzas-doces','Pizzas Doces','🍫','churros','Churros','Doce de leite, canela e açúcar','Grande',8,54],
    ['pizzas-doces','Pizzas Doces','🍫','churros','Churros','Doce de leite, canela e açúcar','Familia',12,70],
    ['pizzas-doces','Pizzas Doces','🍫','m&amp;m','M&M\'s','Chocolate ao leite e M&M\'s','Broto',4,36],
    ['pizzas-doces','Pizzas Doces','🍫','m&amp;m','M&M\'s','Chocolate ao leite e M&M\'s','Media',6,48],
    ['pizzas-doces','Pizzas Doces','🍫','m&amp;m','M&M\'s','Chocolate ao leite e M&M\'s','Grande',8,62],
    ['pizzas-doces','Pizzas Doces','🍫','m&amp;m','M&M\'s','Chocolate ao leite e M&M\'s','Familia',12,80],
    ['bebidas','Bebidas','🥤','coca-2l','Coca-Cola 2L','Refrigerante Coca-Cola 2 litros','2L',null,12],
    ['bebidas','Bebidas','🥤','guarana-2l','Guaraná 2L','Refrigerante Guaraná Antarctica 2 litros','2L',null,10],
    ['bebidas','Bebidas','🥤','fanta-2l','Fanta Laranja 2L','Refrigerante Fanta Laranja 2 litros','2L',null,10],
    ['bebidas','Bebidas','🥤','coca-lata','Coca-Cola Lata','Refrigerante Coca-Cola lata 350ml','350ml',null,6],
    ['bebidas','Bebidas','🥤','guarana-lata','Guaraná Lata','Refrigerante Guaraná lata 350ml','350ml',null,5],
    ['bebidas','Bebidas','🥤','suco-laranja','Suco de Laranja','Suco natural de laranja 500ml','500ml',null,8],
    ['bebidas','Bebidas','🥤','suco-uva','Suco de Uva','Suco integral de uva 500ml','500ml',null,8],
    ['bebidas','Bebidas','🥤','agua-500','Água 500ml','Água mineral sem gás','500ml',null,3],
    ['bebidas','Bebidas','🥤','agua-gas','Água c/ Gás','Água mineral com gás 500ml','500ml',null,4],
    ['bebidas','Bebidas','🥤','cerveja','Cerveja Pilsen','Cerveja pilsen 600ml','600ml',null,8]
  ];
  for (var i=0;i<d.length;i++) sheet.appendRow(d[i]);
  SpreadsheetApp.getUi().alert('Cardápio populado com '+d.length+' itens!');
}
