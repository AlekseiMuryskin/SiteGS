var DMap = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 22: 22, 23: 23, 24: 24, 25: 25, 26: 26, 27: 27, 28: 28, 29: 29, 30: 30, 31: 31, 32: 32, 33: 33, 34: 34, 35: 35, 36: 36, 37: 37, 38: 38, 39: 39, 40: 40, 41: 41, 42: 42, 43: 43, 44: 44, 45: 45, 46: 46, 47: 47, 48: 48, 49: 49, 50: 50, 51: 51, 52: 52, 53: 53, 54: 54, 55: 55, 56: 56, 57: 57, 58: 58, 59: 59, 60: 60, 61: 61, 62: 62, 63: 63, 64: 64, 65: 65, 66: 66, 67: 67, 68: 68, 69: 69, 70: 70, 71: 71, 72: 72, 73: 73, 74: 74, 75: 75, 76: 76, 77: 77, 78: 78, 79: 79, 80: 80, 81: 81, 82: 82, 83: 83, 84: 84, 85: 85, 86: 86, 87: 87, 88: 88, 89: 89, 90: 90, 91: 91, 92: 92, 93: 93, 94: 94, 95: 95, 96: 96, 97: 97, 98: 98, 99: 99, 100: 100, 101: 101, 102: 102, 103: 103, 104: 104, 105: 105, 106: 106, 107: 107, 108: 108, 109: 109, 110: 110, 111: 111, 112: 112, 113: 113, 114: 114, 115: 115, 116: 116, 117: 117, 118: 118, 119: 119, 120: 120, 121: 121, 122: 122, 123: 123, 124: 124, 125: 125, 126: 126, 127: 127, 1027: 129, 8225: 135, 1046: 198, 8222: 132, 1047: 199, 1168: 165, 1048: 200, 1113: 154, 1049: 201, 1045: 197, 1050: 202, 1028: 170, 160: 160, 1040: 192, 1051: 203, 164: 164, 166: 166, 167: 167, 169: 169, 171: 171, 172: 172, 173: 173, 174: 174, 1053: 205, 176: 176, 177: 177, 1114: 156, 181: 181, 182: 182, 183: 183, 8221: 148, 187: 187, 1029: 189, 1056: 208, 1057: 209, 1058: 210, 8364: 136, 1112: 188, 1115: 158, 1059: 211, 1060: 212, 1030: 178, 1061: 213, 1062: 214, 1063: 215, 1116: 157, 1064: 216, 1065: 217, 1031: 175, 1066: 218, 1067: 219, 1068: 220, 1069: 221, 1070: 222, 1032: 163, 8226: 149, 1071: 223, 1072: 224, 8482: 153, 1073: 225, 8240: 137, 1118: 162, 1074: 226, 1110: 179, 8230: 133, 1075: 227, 1033: 138, 1076: 228, 1077: 229, 8211: 150, 1078: 230, 1119: 159, 1079: 231, 1042: 194, 1080: 232, 1034: 140, 1025: 168, 1081: 233, 1082: 234, 8212: 151, 1083: 235, 1169: 180, 1084: 236, 1052: 204, 1085: 237, 1035: 142, 1086: 238, 1087: 239, 1088: 240, 1089: 241, 1090: 242, 1036: 141, 1041: 193, 1091: 243, 1092: 244, 8224: 134, 1093: 245, 8470: 185, 1094: 246, 1054: 206, 1095: 247, 1096: 248, 8249: 139, 1097: 249, 1098: 250, 1044: 196, 1099: 251, 1111: 191, 1055: 207, 1100: 252, 1038: 161, 8220: 147, 1101: 253, 8250: 155, 1102: 254, 8216: 145, 1103: 255, 1043: 195, 1105: 184, 1039: 143, 1026: 128, 1106: 144, 8218: 130, 1107: 131, 8217: 146, 1108: 186, 1109: 190}

function UnicodeToWin1251(s) {
    var L = []
    for (var i=0; i<s.length; i++) {
        var ord = s.charCodeAt(i)
        if (!(ord in DMap))
            throw "Character "+s.charAt(i)+" isn't supported by win1251!"
        L.push(String.fromCharCode(DMap[ord]))
    }
    return L.join('')
}
(function($){
	$.fn.extend({
		csvExport: function(options) {
			this.defaultOptions = {
				escapeContent: true,
				title: 'Exported_Table.csv',
				beforeStart: function() {},
				onStringReady: function() {}
			};

			const settings = $.extend({}, this.defaultOptions, options);

			//MULTIPLE OBJECTS HANDLER
			return this.each(function() {
				const $this = $(this);
				const real = {
					x: 0,
					y: 0
				};
				// Objects to insert : { ori : {x:0,y:O}, toDo : xxx, done : xxx }
				const toExpand = {
					x: [],
					y: []
				};
				let theString = '';

				function deleteChecker(parent, pos){
					if(parent[pos].toDo == parent[pos].done){
						parent.splice(pos, pos+1);

						return true;
					}

					return false;
				}

				function spanChecker(){
					let colspanHandler = true;

					while(colspanHandler){
						let broken = false,
							directions = ['y', 'x'];

						for(let k = 0; k< directions.length; k++){
							const direction = directions[k];
							const other = direction == 'y' ? 'x' : 'y';

							for(let i = 0; i < toExpand[direction].length; i++){

								// Move on if task done
								if(deleteChecker(toExpand[direction], i) && i > 0){
									i--;
								}

								if(toExpand[direction].length > 0){
									if(real[other] == toExpand[direction][i].ori[other]){
										if(real[direction] == toExpand[direction][i].ori[direction] + toExpand[direction][i].done){
											theString+='"",';
											toExpand[direction][i].done++;
											broken=true;
											real.x++;
											break;
										}
									}
								}
							}
						}

						if(!broken) colspanHandler=false;
					}
				}

				function contentCheckup(data){
					if(settings.escapeContent) return data.replace(/([\\"])/g, '\\$1');

					return data;
				}

				function b64toBlob(b64Data, contentType, sliceSize) {
					contentType = contentType || '';
					sliceSize = sliceSize || 512;

					let byteCharacters = atob(b64Data);
					let byteArrays = [];

					for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
						let slice = byteCharacters.slice(offset, offset + sliceSize),
							byteNumbers = new Array(slice.length);

						for (let i = 0; i < slice.length; i++) {
							byteNumbers[i] = slice.charCodeAt(i);
						}

						let byteArray = new Uint8Array(byteNumbers);

						byteArrays.push(byteArray);
					}

					let blob = new Blob(byteArrays, {type: contentType});

					return blob;
				}

				//BEFORESTART CALLBACK
				settings.beforeStart.call(null, $this);

				$('tr', $this).each(function(){
					const currentTR = $(this);

					currentTR.children().each(function(){
						const currentTD = $(this);

						spanChecker();

						/* CURRENT TD HANDLER __START */
						if(currentTD.is('[colspan]')){
							toExpand.x.push({
								ori: {
									x: real.x,
									y: real.y
								},
								toDo: +currentTD.attr('colspan'),
								done: 1
							});
						}

						if(currentTD.is('[rowspan]')){
							toExpand.y.push({
								ori: {
									x: real.x,
									y: real.y
								},
								toDo: +currentTD.attr('rowspan'),
								done: 1
							});
						}

						let currentCellString = '',
							currentCellNodes = currentTD[0].childNodes;

						for(let i = 0; i < currentCellNodes.length; i++){
							currentCellString += (currentCellNodes[i].innerText || currentCellNodes[i].textContent.replace(/\s/g, '').length ? currentCellNodes[i].textContent : '') + ' ';
						}
						currentCellString = contentCheckup(currentCellString).trim();

						theString+='"'+currentCellString+'";';
						real.x++;
						/* CURRENT TD HANDLER __END */
					});

					theString = theString.substring(0, theString.length - 1);
					theString+='\r\n';
					real.x=0;
					real.y++;
				});

				settings.onStringReady.call(null, theString);

				const
					fileData = window.btoa(UnicodeToWin1251(theString)),// window.btoa(unescape(encodeURIComponent(theString))),
					title = settings.title;

				// IE Fix
				if(navigator.userAgent.indexOf('MSIE ') > 0 || navigator.userAgent.match(/Trident.*rv\:11\./)){
					const blobObject = b64toBlob(fileData);

					window.navigator.msSaveOrOpenBlob(blobObject, title);
				}else{
					const a = document.createElement('a');

					a.href = 'data:application/vnd.ms-excel;base64,' + fileData;

					a.download = title;

					// Append to current DOM to allow click trigger
					a.style.display = 'none';
					document.body.appendChild(a);

					a.click();

					// Cleanup
					a.remove();
				}
			});
		}
	});
}(jQuery));