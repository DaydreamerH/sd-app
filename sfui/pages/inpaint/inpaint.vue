<template>
	<view class="row"  @touchmove.stop.prevent="() => {}">
		<view ref='img'style='display: flex;height: auto;'>
			<img :src='img_file' class='img' @load='after_img'>
			<canvas class="mycanvas" canvas-id="mycanvas" @touchstart="touchstart" @touchmove="touchmove"
			@touchend="touchend" ref='canvas' :style="{'height':c_height+'rpx'}"></canvas>
		</view>
		<view>
			<button @click='finish'>保存</button>
		</view>
	</view>
</template>

<script>
	import {
		pathToBase64,
		base64ToPath
	} from 'image-tools'
	var x = 20;
	var y = 20;
	export default {
		data() {
			return {
				ctx: '', //绘图图像
				points: [], //路径点集合 
				img_file: '',
				c_height: 0
			}
		},
		onLoad(option) {
			this.img_file = option.img_file
		},
		methods: {
			after_img(e) {
				// this.c_height = e.target.height 
				// console.log(this.c_height)
				let _this = this
				uni.getImageInfo({
					src:_this.img_file,
					success(image){
						let hole_wh = image.width+image.height
						let imgWidth = (image.width/hole_wh)
						let imgHeight = (image.height/hole_wh)
						let img_bl = Math.ceil(750/imgWidth)
						_this.c_height = img_bl*imgHeight
						console.log(img_bl,_this.c_height,image.width)
					}
				})
				this.ctx = uni.createCanvasContext("mycanvas", this); //创建绘图对象
				this.ctx.lineWidth = 8;
				this.ctx.lineCap = "round"
				this.ctx.lineJoin = "round"
			},
			//触摸开始，获取到起点
			touchstart: function(e) {
				let startX = e.changedTouches[0].x;
				let startY = e.changedTouches[0].y;
				let startPoint = {
					X: startX,
					Y: startY
				};

				/* **************************************************
					#由于uni对canvas的实现有所不同，这里需要把起点存起来
				 * **************************************************/
				this.points.push(startPoint);

				//每次触摸开始，开启新的路径
				this.ctx.beginPath();
			},

			//触摸移动，获取到路径点
			touchmove: function(e) {
				let moveX = e.changedTouches[0].x;
				let moveY = e.changedTouches[0].y;
				let movePoint = {
					X: moveX,
					Y: moveY
				};
				this.points.push(movePoint); //存点
				let len = this.points.length;
				if (len >= 2) {
					this.draw(); //绘制路径
				}

			},

			// 触摸结束，将未绘制的点清空防止对后续路径产生干扰
			touchend: function() {
				this.points = [];
			},

			/* ***********************************************
			#   绘制笔迹
			#	1.为保证笔迹实时显示，必须在移动的同时绘制笔迹
			#	2.为保证笔迹连续，每次从路径集合中区两个点作为起点（moveTo）和终点(lineTo)
			#	3.将上一次的终点作为下一次绘制的起点（即清除第一个点）
			************************************************ */
			draw: function() {
				let point1 = this.points[0]
				let point2 = this.points[1]
				this.points.shift()
				this.ctx.moveTo(point1.X, point1.Y)
				this.ctx.lineTo(point2.X, point2.Y)
				this.ctx.stroke()
				this.ctx.draw(true)

			},

			//清空画布
			clear: function() {
				let that = this;
				uni.getSystemInfo({
					success: function(res) {
						let canvasw = res.windowWidth;
						let canvash = res.windowHeight;
						that.ctx.clearRect(0, 0, canvasw, canvash);
						that.ctx.draw(true);
					},
				})
			},

			//完成绘画并保存到本地
			finish: function() {
				this.ctx.draw(true,()=>{
					uni.canvasToTempFilePath({
						canvasId: 'mycanvas',
						fileType:"jpg",
						success: function(res) {
							let path = res.tempFilePath;
							pathToBase64(path).then(base64 => {
								uni.setStorageSync('mask',base64)
							}).catch(e => {
								console.log(e)
							})
						}
					})
				})
			}
		},
	}
</script>

<style>
	.row {
		width: 750rpx;
		height: 100%;
		overflow-y: hidden;
	}

	.mycanvas {
		position: absolute;
		top: 0;
		left: 0;
		z-index: 3;
		width: 750rpx;
		height: auto;
	}

	.img {
		width: 750rpx;
		height: auto;
	}
</style>