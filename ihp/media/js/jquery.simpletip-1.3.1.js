/**
 * jquery.simpletip 1.3.1. A simple tooltip plugin
 * 
 * Copyright (c) 2009 Craig Thompson
 * http://craigsworks.com
 *
 * Licensed under GPLv3
 * http://www.opensource.org/licenses/gpl-3.0.html
 *
 * Launch  : February 2009
 * Version : 1.3.1
 * Released: February 5, 2009 - 11:04am
 */
(function($){

   function Simpletip(elem, conf)
   {
      var self = this;
      elem = jQuery(elem);
      
      var tooltip = jQuery(document.createElement('div'))
                     .addClass(conf.baseClass)
                     .addClass( (conf.fixed) ? conf.fixedClass : '' )
                     .addClass( (conf.persistent) ? conf.persistentClass : '' )
                     .html(conf.content)
                     .appendTo(elem);
      
      if(!conf.hidden) tooltip.show();
      else tooltip.hide();
      
      if(!conf.persistent)
      {
         elem.hover(
            function(event){ self.show(event) },
            function(){ self.hide() }
         );
         
         if(!conf.fixed)
         {
            elem.mousemove( function(event){ 
               if(tooltip.css('display') !== 'none') self.updatePos(event); 
            });
         };
      }
      else
      {
         elem.click(function(event)
         {
            if(event.target === elem.get(0))
            {
               if(tooltip.css('display') !== 'none')
                  self.hide();
               else
                  self.show();
            };
         });
         
         jQuery(window).mousedown(function(event)
         { 
            if(tooltip.css('display') !== 'none')
            {
               var check = (conf.focus) ? jQuery(event.target).parents('.tooltip').andSelf().filter(function(){ return this === tooltip.get(0) }).length : 0;
               if(check === 0) self.hide();
            };
         });
      };
      
      
      jQuery.extend(self,
      {
         getVersion: function()
         {
            return [1, 2, 0];
         },
         
         getParent: function()
         {
            return elem;
         },
         
         getTooltip: function()
         {
            return tooltip;
         },
         
         getPos: function()
         {
            return tooltip.offset();
         },
         
         setPos: function(posX, posY)
         {
            var elemPos = elem.position(); // changed from offset()
            
            if(typeof posX == 'string') posX = parseInt(posX) + elemPos.left;
            if(typeof posY == 'string') posY = parseInt(posY) + elemPos.top;
            
            tooltip.css({ left: posX, top: posY });
            
            return self;
         },
         
         show: function(event)
         {
            conf.onBeforeShow.call(self);
            
            self.updatePos( (conf.fixed) ? null : event );
            
            switch(conf.showEffect)
            {
               case 'fade': 
                  tooltip.fadeIn(conf.showTime); break;
               case 'slide': 
                  tooltip.slideDown(conf.showTime, self.updatePos); break;
               case 'custom':
                  conf.showCustom.call(tooltip, conf.showTime); break;
               default:
               case 'none':
                  tooltip.show(); break;
            };
            
            tooltip.addClass(conf.activeClass);
            
            conf.onShow.call(self);
            
            return self;
         },
         
         hide: function()
         {
            conf.onBeforeHide.call(self);
            
            switch(conf.hideEffect)
            {
               case 'fade': 
                  tooltip.fadeOut(conf.hideTime); break;
               case 'slide': 
                  tooltip.slideUp(conf.hideTime); break;
               case 'custom':
                  conf.hideCustom.call(tooltip, conf.hideTime); break;
               default:
               case 'none':
                  tooltip.hide(); break;
            };
            
            tooltip.removeClass(conf.activeClass);
            
            conf.onHide.call(self);
            
            return self;
         },
         
         update: function(content)
         {
            tooltip.html(content);
            conf.content = content;
            
            return self;
         },
         
         load: function(uri, data)
         {
            conf.beforeContentLoad.call(self);
            
            tooltip.load(uri, data, function(){ conf.onContentLoad.call(self); });
            
            return self;
         },
         
         boundryCheck: function(posX, posY)
         {
            var tooltipPos = {};
            tooltipPos.l = posX;
            tooltipPos.t = posY;
            tooltipPos.r = tooltipPos.l + tooltip.outerWidth();
            tooltipPos.b = tooltipPos.t + tooltip.outerHeight();
            
            var jwin = jQuery(window);
            var visible = {};
            visible.l = jwin.scrollLeft();
            visible.t = jwin.scrollTop();
            visible.r = visible.l + jwin.width();
            visible.b = visible.t + jwin.height();
            
            // default to no adjustment
            var adjustment = [0, 0];
			
			/*
            alert("visible = " + visible.l + "," + visible.t + ":" +
               visible.r + "," + visible.b + ";\n" +
               "tooltip pos = " + tooltipPos.l + "," + tooltipPos.t + ":" +
               tooltipPos.r + "," + tooltipPos.b + ";\n" +
               "adjustment = " + adjustment[0] + "," + adjustment[1]);
            */
            
            // does tooltip extend past the bottom right of the visible area?
            if (visible.r < tooltipPos.r) adjustment[0] = visible.r - tooltipPos.r;
            if (visible.b < tooltipPos.b) adjustment[1] = visible.b - tooltipPos.b;

			/*
            alert("shift up:\n" +
               "visible = " + visible.l + "," + visible.t + ":" +
               visible.r + "," + visible.b + ";\n" +
               "tooltip = " + tooltipPos.l + "," + tooltipPos.t + ":" +
               tooltipPos.r + "," + tooltipPos.b + ";\n" +
               "adjustment = " + adjustment[0] + "," + adjustment[1]);
            */
            
            // apply adjustment to see if it takes the tooltip off top/left of screen
            // we could ignore tooltipPos.r and tooltipPos.b because we don't need them any more
            tooltipPos.l = tooltipPos.l + adjustment[0];
            tooltipPos.t = tooltipPos.t + adjustment[1];
            tooltipPos.r = tooltipPos.r + adjustment[0];
            tooltipPos.b = tooltipPos.b + adjustment[1];
            
            // does tooltip (now) start above the top left of the visible area?
            if (visible.l > tooltipPos.l) adjustment[0] = adjustment[0] + visible.l - tooltipPos.l;
            if (visible.t > tooltipPos.t) adjustment[1] = adjustment[1] + visible.t - tooltipPos.t;
            
            /*
            alert("shift down:\n" +
               "visible = " + visible.l + "," + visible.t + ":" +
               visible.r + "," + visible.b + ";\n" +
               "tooltip = " + tooltipPos.l + "," + tooltipPos.t + ":" +
               tooltipPos.r + "," + tooltipPos.b + ";\n" +
               "adjustment = " + adjustment[0] + "," + adjustment[1]);
            */
            
            return adjustment;
         },
         
         updatePos: function(event)
         {
            var tooltipWidth = tooltip.outerWidth();
            var tooltipHeight = tooltip.outerHeight();
            
            if(!event && conf.fixed)
            {
               if(conf.position.constructor == Array)
               {
                  posX = parseInt(conf.position[0]);
                  posY = parseInt(conf.position[1]);
               }
               else if(jQuery(conf.position).attr('nodeType') === 1)
               {
                  var offset = jQuery(conf.position).offset();
                  posX = offset.left;
                  posY = offset.top;
               }
               else
               {
                  var elemPos = elem.position(); // changed from offset();
                  var elemWidth = elem.outerWidth();
                  var elemHeight = elem.outerHeight();
                  
                  switch(conf.position)
                  {
                     case 'top':
                        var posX = elemPos.left - (tooltipWidth / 2) + (elemWidth / 2);
                        var posY = elemPos.top - tooltipHeight;
                        break;
                        
                     case 'bottom':
                        var posX = elemPos.left - (tooltipWidth / 2) + (elemWidth / 2);
                        var posY = elemPos.top + elemHeight;
                        break;
                     
                     case 'left':
                        var posX = elemPos.left - tooltipWidth;
                        var posY = elemPos.top - (tooltipHeight / 2) + (elemHeight / 2);
                        break;
                        
                     case 'right':
                        var posX = elemPos.left + elemWidth;
                        var posY = elemPos.top - (tooltipHeight / 2) + (elemHeight / 2);
                        break;
                     
                     default:
                     case 'default':
                        var posX = (elemWidth / 2) + elemPos.left + 20;
                        var posY = elemPos.top;
                        break;
                  };
               };
            }
            else
            {
               var posX = event.pageX;
               var posY = event.pageY;
            };
            
            if(typeof conf.position != 'object')
            {
               posX = posX + conf.offset[0];
               posY = posY + conf.offset[1]; 
               
               if(conf.boundryCheck)
               {
                  // boundryCheck needs the screen position, not the offset(),
                  // to see whether the element overflows the screen; but the
                  // CSS position is relative to the offset parent, not the
                  // screen.
                  
                  var offsetFromOffsetParent = elem.position();
                  var offsetFromDocumentOrigin = elem.offset();
                  var offsetOfOffsetParent = {
                     x: offsetFromDocumentOrigin.left - offsetFromOffsetParent.left,
                     y: offsetFromDocumentOrigin.top  - offsetFromOffsetParent.top
                  };
                  
                  var adjustment = self.boundryCheck(posX + offsetOfOffsetParent.x,
                     posY + offsetOfOffsetParent.y);
                  
                  /*
                  alert("adjust posX from " + posX + " by " + overflow[0] +
                     "pixels");
                  */
                  
                  posX = posX + adjustment[0];
                  posY = posY + adjustment[1];
               }
            }
            else
            {
               if(typeof conf.position[0] == "string") posX = String(posX);
               if(typeof conf.position[1] == "string") posY = String(posY);
            };
            
            self.setPos(posX, posY);
            
            return self;
         }
      });
   };
   
   jQuery.fn.simpletip = function(conf)
   { 
      // Check if a simpletip is already present
      var api = jQuery(this).eq(typeof conf == 'number' ? conf : 0).data("simpletip");
      if(api) return api;
      
      // Default configuration
      var defaultConf = {
         // Basics
         content: 'A simple tooltip',
         persistent: false,
         focus: false,
         hidden: true,
         
         // Positioning
         position: 'default',
         offset: [0, 0],
         boundryCheck: true,
         fixed: true,
         
         // Effects
         showEffect: 'fade',
         showTime: 150,
         showCustom: null,
         hideEffect: 'fade',
         hideTime: 150,
         hideCustom: null,
         
         // Selectors and classes
         baseClass: 'tooltip',
         activeClass: 'active',
         fixedClass: 'fixed',
         persistentClass: 'persistent',
         focusClass: 'focus',
         
         // Callbacks
         onBeforeShow: function(){},
         onShow: function(){},
         onBeforeHide: function(){},
         onHide: function(){},
         beforeContentLoad: function(){},
         onContentLoad: function()
         {
            // If some content has been loaded, need to reposition the tooltip
            this.updatePos();
         }
      };
      jQuery.extend(defaultConf, conf);
      
      this.each(function()
      {
         var el = new Simpletip(jQuery(this), defaultConf);
         jQuery(this).data("simpletip", el);  
      });
      
      return this; 
   };
})();