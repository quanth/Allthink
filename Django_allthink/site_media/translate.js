

///////////////////////// MEMLIB /////////////////////////
// Translation functions
//////////////////////////////////////////////////////////

var phrasesFound		= new Array();
var phrasesTranslated	= new Array();
var phraseKeys			= new Array();
var lc				 	= (navigator.userLanguage) ? navigator.userLanguage : window.navigator.language;
var browserLanguage		= lc.split('-')[0].toLowerCase().replace(/[^a-z]/g,'');
var cookieLanguage		= (getCookie('language')) ? getCookie('language').toLowerCase().replace(/[^a-z]/g,'') : false;
var language			= 'en';




// Initiate translation
function translate () {

	// get user's language
	if (getParam('language'))		language=getParam('language').toLowerCase().replace(/[^a-z]/g,'');
	else if (cookieLanguage)		language=cookieLanguage;
	else							language=browserLanguage;

	// highlight language on page
	if (document.getElementById('language-'+language)) 
		document.getElementById('language-'+language).className+=' selected';

	// Language Cookie
	if (language==browserLanguage && cookieLanguage)				setCookie('language',language,0);
	else if (language!=browserLanguage && cookieLanguage!=language) setCookie('language',language,365);
	
	
	if (language!='en' && typeof(NOTRANSLATE)==='undefined') {
		findPhrases(document);
		translatePhrases();
	}
}


// Find native language phrases in document
function findPhrases (obj) {
	
	if ((!obj.className) || (obj.className.indexOf('notranslate')===-1)) {
		
		if (obj.hasChildNodes()) {
			for (var i=0;i<obj.childNodes.length;i++) findPhrases(obj.childNodes[i]);
		}
		
		else if (
			(obj.nodeValue) && 
			(obj.nodeValue.match(/[a-zA-Z]/)) &&
			(!obj.parentElement || !obj.parentElement.tagName || (obj.parentElement.tagName!='SCRIPT' && obj.parentElement.tagName!='STYLE' && obj.parentElement.tagName!='TITLE')) &&
			(obj.constructor.toString().indexOf('Comment')===-1)
		) {
			var str=obj.nodeValue.replace(/[\r\n\t]+/g," ").replace(/\s\s+/g," ").replace(/^[\s]+|[\s]+$/g,"");
			if (str.length>2) phrasesFound.push(str);
		}
		phrasesFound=arrayUnique(phrasesFound);
	}
}


// Send AJAX request to get translations of phrases
function translatePhrases () {
	var q 			= {};
	q['api']		= 'xml';
	q['lang']		= language;
	q['fromurl']	= document.location.href;
	q['phrases']	= phrasesFound.join("\n");
	Req				= newReq2();
	Req['url']		= '/i18n/translate.php';
	Req.todo 		= sortTranslations;
	Req.post		(setQS(q));
}


// Replace all translatable phrases
function sortTranslations () {

	var items=getitems('translations', this.responseXML);
	
	for (var i=0;i<items.length;i++) {
		phrasesTranslated[phrasesFound[items[i]['key']]]	= items[i]['translation'];
		phraseKeys[phrasesFound[items[i]['key']]]			= items[i]['phraseid'];
	}
	replacePhrases(document);
}


// Find native language phrases in document
function replacePhrases (obj) {
	
	if ((!obj.className) || (obj.className.indexOf('notranslate')===-1)) {
	
		if (obj.hasChildNodes()) {
			for (var i=0;i<obj.childNodes.length;i++) replacePhrases(obj.childNodes[i]);
		}
		else if (
			(obj.nodeValue) && 
			(obj.nodeValue.match(/[a-zA-Z]/)) && 
			(	!obj.parentElement || 
				!obj.parentElement.tagName || 
				(	obj.parentElement.tagName!='SCRIPT' && 
					obj.parentElement.tagName!='STYLE' && 
					obj.parentElement.tagName!='TITLE'
				)
			) &&
			(obj.constructor.toString().indexOf('Comment')===-1)
		) {
			var str=obj.nodeValue.replace(/[\r\n\t]+/g," ").replace(/\s\s+/g," ").replace(/^[\s]+|[\s]+$/g,"");
			if ((str.length>2) && (phrasesTranslated[str])) {
			
				// start and end spaces
				var startspace=''; var endspace='';
				if (obj.nodeValue.match(/^[\s\r\n\t]/)) startspace=' ';
				if (obj.nodeValue.match(/[\s\r\n\t]$/)) endspace=' ';
			
				// create new <font> with translation
				var newphrase=document.createElement('font');
				newphrase.innerHTML=startspace+phrasesTranslated[str]+endspace;
				newphrase.phraseid=phraseKeys[str];
				newphrase.ondblclick=function () { 
					var trans=prompt('Translation:',phrasesTranslated[str]);
					if (trans) {
						saveTranslation(this.phraseid,trans);
					}
					return false;
				}
				
				// swap <font> for text
				obj.nodeValue='';
				obj.parentNode.replaceChild(newphrase,obj);
			}
		}
	}
}








///////////////////////// MEMLIB /////////////////////////
// JS AJAX functions
//////////////////////////////////////////////////////////

// Create a new cross-browser AJAX req object
function newReq2 (parent) {
 	var req = false;
	try  			{ req = new XMLHttpRequest(); }
	catch(e) { 
	 	try  		{ req = new ActiveXObject("Msxml2.XMLHTTP"); }
		catch(e) { 
			try  	{ req = new ActiveXObject("Microsoft.XMLHTTP"); }
			catch(e) { 
				alert('Your browser is too old to use this site, go to www.mozilla.com to download Firefox.');
			}
		}
	}
	req.post				= AjaxPost;
	req.get 				= AjaxGet;
	req.onreadystatechange 	= reqChangeState2;
	
	if (parent) req.parent = parent;
	
	return req;
}




// Ajax times out
function reqTimeOut () {
	document.location.reload();
}



// Generic AJAX POST function
function AjaxPost (query) {
	if (query)						this.query		= query;
	
	this.to		 					= setTimeout('reqTimeOut()', 10000);
	this.open						("POST", this.url, true);
	this.setRequestHeader			('Content-type', 'application/x-www-form-urlencoded; charset=UTF-8'); 
	this.setRequestHeader			("Content-length", this.query.length);
	this.send						(this.query);
}


// Generic AJAX GET function
function AjaxGet () {
	this.to		 					= setTimeout('reqTimeOut()', 10000);
	this.open						("GET", this.url, true);
	this.send						();
}


// Handle AJAX state changes
function reqChangeState2 () {
	if (this.readyState == 4) {
		clearTimeout(this.to);

		if (this.responseXML) {	
			// parse XML data
			this.J				= new Object();
		 	this.J.success		= getvalue('success', this.responseXML);
			this.J.values		= xml2object(getchild('values', this.responseXML));
			this.J.errors		= xml2object(getchild('errors', this.responseXML));
		
			// success and failure functions
			if (this.J.success == 'true') { if (this.todo) this.todo(); }
			else alert('Error: '+getvalue('message', this.responseXML));
		}
	}
}


// Convert object to query string
function setQS (obj) {
	var pairs=new Array();
	for (var k in obj) {
		pairs.push(encodeURIComponent(k)+'='+encodeURIComponent(obj[k]));
	}
	return pairs.join('&');
}



// Get query parameter value
function getParam (key) {
	var pairs = window.location.search.substring(1).split("&");
	for (i=0;i<pairs.length;i++) {
		arr = pairs[i].split("=");
		if (arr[0] == key) return arr[1];
	}
}



// Remove array duplicates
function arrayUnique (arr) {
    var a = [];
    var found = {};
    for(var i=0; i<arr.length; i++) {
		if (!found[arr[i]]) {
			a.push(arr[i]);
			found[arr[i]]=1;
		}
	}
	return a;
}



/// COOKIES
function setCookie(c_name,value,exdays) {
	var exdate=new Date();
	exdate.setDate(exdate.getDate() + exdays);
	document.cookie=c_name + "=" + escape(value) + "; path=/; domain=engrade.com; expires="+exdate.toUTCString();
}


function getCookie(c_name) {
	var i,x,y,ARRcookies=document.cookie.split(";");
	for (i=0;i<ARRcookies.length;i++) {
		x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
		y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
		x=x.replace(/^\s+|\s+$/g,"");
		if (x==c_name) return unescape(y);
	}
}




/// EXECUTE
translate();

