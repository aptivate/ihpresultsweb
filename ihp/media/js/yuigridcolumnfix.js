/*
	YUI grids columnfix 
	written by Christian Heilmann (http://wait-till-i.com)
	either just include or call with YAHOO.util.grids.columnfix.fix(gridgroup);
*/
YAHOO.namespace('util.grids');
YAHOO.util.grids.columnfix = function(){
	function fixcolumns(){
		var tofix = YAHOO.util.Dom.getElementsByClassName('columnfix','div',this);
		var divs = tofix.length > 0 ? tofix : this.getElementsByTagName('div');
		for(var i=0;divs[i];i++){
			if(divs[i].className.indexOf('yui-g') !== -1){
				fix(divs[i]);
			};
		};
	};
	function fix(grid){
		if(YAHOO.util.Dom.inDocument(grid)){
			var region = YAHOO.util.Dom.getRegion(grid);
			var height = region.bottom - region.top;
			var columns = YAHOO.util.Dom.getElementsByClassName('yui-u','div',grid);
			for(var i=0;columns[i];i++){
				YAHOO.util.Dom.setStyle(columns[i],'height',height+'px');
			};
		}
	};	
	YAHOO.util.Event.onContentReady('yui-main',fixcolumns);
	return{fix:fix};
}();
