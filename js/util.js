/*
 * util.js
 */

// jquery required

function console_init() 
{
	if( !("console" in window) ) 
	{
		// firebug methods
		var names = [ "log", "debug", "info", "warn", "error", "assert", "dir", "dirxml" 
		    ,"group", "groupEnd", "time", "timeEnd", "count", "trace", "profile", "profileEnd" ];
		window.console = {};
		for( var i = 0; i < names.length; ++i ) 
			window.console[names[i]] = function() {};
			
		// custom window logging
//		window.console.debug  = function(s) { window.log( 'debug: '+s, 1 ); }
//		window.console.info   = function(s) { window.log( 'info: '+s, 0 ); }
//		window.console.warn   = function(s) { window.log( 'warn: '+s, -1 ); }
//		window.console.error  = function(s) { window.log( 'error: '+s, -2 ); }
//		window.console.assert = function(s) { window.log( 'assert: '+s, -3 ); }
	}
}

function focus_input( name )
{
	$(document).ready( function(){ $("input[name="+name+"]").focus(); } )
}

function dash_tail( s )
{
	var i = s.lastIndexOf('-')
	return (i >= 0)? s.substring(i+1): "";
}

/* KLADR */

KLADR_FLDPOS = [ 0, 2, 5, 8, 11, 15 ]

function kladr_subcode( code, level )
{
	if( level < 1 ) return '';
	if( level > 5 ) level = 5;
	return code.substring( 0, KLADR_FLDPOS[level] );
}

function kladr_codelevel( code )
{
	var level = 0;
	try {
		if( parseInt( code.substring( KLADR_FLDPOS[0], KLADR_FLDPOS[1] ) ) ) level = 1;
		if( parseInt( code.substring( KLADR_FLDPOS[1], KLADR_FLDPOS[2] ) ) ) level = 2;
		if( parseInt( code.substring( KLADR_FLDPOS[2], KLADR_FLDPOS[3] ) ) ) level = 3;
		if( parseInt( code.substring( KLADR_FLDPOS[3], KLADR_FLDPOS[4] ) ) ) level = 4;
		if( parseInt( code.substring( KLADR_FLDPOS[4], KLADR_FLDPOS[5] ) ) ) level = 5;
	}
	catch( ign ) { }
	
//	alert( 'cl: '+level+' '+code )
	return level;
}

function kladr_list( code, level )
{
	$.get( '/kladr/list/'+code+':'+level )
}

function kladr_setoptions( sel, code, level, opts )
{
	var sc = kladr_subcode( code, level )
	sel.html( "<option value='0'>&nbsp;</option>" )
	for( var i=0; i < opts.length; i++ )
	{
		var elem = $( "<option></option>" ).attr( 'value', opts[i][0] ).text( opts[i][1] )
		if( (sc == kladr_subcode( opts[i][0], level )) ) { elem.attr( 'selected', '1' ) }
		sel.append( elem ) 
	}
}


function kladr_load_sel( code, lvl0, lvl1 )
{
	for( var i=lvl0+1; i <= lvl1; i++ )
	{
		$("#kladr_s"+i).html( "<option value='0'>&nbsp;</option>" )
	}

	/* todo: refactor with 'create function' */
	if( lvl0 < 1 && 1 <= lvl1 ) {
		$.getJSON( '/kladr/list/'+code+':1', 
			function(data) { kladr_setoptions( $("#kladr_s1"), code, 1, data ) } )
	}
	if( lvl0 < 2 && 2 <= lvl1 ) {
		$.getJSON( '/kladr/list/'+code+':2', 
			function(data) { kladr_setoptions( $("#kladr_s2"), code, 2, data ) } )
	}
	if( lvl0 < 3 && 3 <= lvl1 ) {
		$.getJSON( '/kladr/list/'+code+':3', 
			function(data) { kladr_setoptions( $("#kladr_s3"), code, 3, data ) } )
	}
	if( lvl0 < 4 && 4 <= lvl1 ) {
		$.getJSON( '/kladr/list/'+code+':4', 
			function(data) { kladr_setoptions( $("#kladr_s4"), code, 4, data ) } )
	}
	if( lvl0 < 5 && 5 <= lvl1 ) {
		$.getJSON( '/kladr/list/'+code+':5', 
			function(data) { kladr_setoptions( $("#kladr_s5"), code, 5, data ) } )
	}
}

function kladr_select( fld, level )
{
	var v = $(fld).find("option:selected").val()
	while( v == '0' && level > 1 ) {
		level--;
		v = $("#kladr_s"+level).find("option:selected").val()
	}
	$("#id_addr_code").val( v )
	kladr_set_text( v )
	kladr_load_sel( v, level, 5 )
}

function kladr_set_text( code )
{
	if( !code ) { code = $("#id_addr_code").val() }
	$.getJSON( '/kladr/text/'+code, function(data) {
		var b = $("#id_addr_build").val().trim()
		var f = $("#id_addr_flat").val().trim()
		var v = data
		if( b.length ) { v += ', '+b; }
		if( f.length ) { v += ', '+f; }
		$("#id_addr_text").val(v)
		$("#addr_text_displ").text(v)
	})
}

function kladr_onload()
{
	var code = $("#id_addr_code").val()
	kladr_load_sel( code, 0, 5 )
//	kladr_set_text( code )
	
	$("#kladr_s1").change( function() { kladr_select( this, 1 ); } )
	$("#kladr_s2").change( function() { kladr_select( this, 2 ); } )
	$("#kladr_s3").change( function() { kladr_select( this, 3 ); } )
	$("#kladr_s4").change( function() { kladr_select( this, 4 ); } )
	$("#kladr_s5").change( function() { kladr_select( this, 5 ); } )
	
	$("#id_addr_build").change( function() { kladr_set_text(); } )
	$("#id_addr_flat").change( function() { kladr_set_text(); } )
}

//.
