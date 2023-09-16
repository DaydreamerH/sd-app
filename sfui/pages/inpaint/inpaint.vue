<template>
	<view class="row" @touchmove.stop.prevent="() => {}">
		<uv-toast ref='toast'></uv-toast>
		<view ref='img' style='display: flex;height: auto;margin-bottom: 10rpx;'>
			<img :src='img_file' class='img' @load='after_img' id='image'>
			<canvas class="mycanvas" canvas-id="mycanvas" @touchstart="touchstart" @touchmove="touchmove"
				@touchend="touchend" ref='canvas' :style="{'height':c_height+'rpx'}"></canvas>
		</view>
		<view class='info'>
			通过触摸屏幕对图像进行涂抹，经涂抹的部分将被重绘，而未被涂抹的部分将不会改变，以此实现部分内容的精确修改
		</view>
		<view class='button_area'>
			<uv-button class="delete_button" icon='trash' iconColor="white" color="#FF5A5F" @click="clear"></uv-button>
			<uv-button class="delete_button" icon='checkbox-mark' iconColor="white" color="#FF5A5F"
				@click="finish"></uv-button>
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
		onShow() {
				this.img_file = uni.getStorageSync('img_file')
				uni.removeStorageSync('img_file')
		},
		methods: {
			after_img(e) {
				// this.c_height = e.target.height 
				// console.log(this.c_height)
				// let _this = this
				// if(this.img_file.length<200)
				// 	uni.getImageInfo({
				// 		src: _this.img_file,
				// 		success(image) {
				// 			let hole_wh = image.width + image.height
				// 			let imgWidth = (image.width / hole_wh)
				// 			let imgHeight = (image.height / hole_wh)
				// 			let img_bl = Math.ceil(750 / imgWidth)
				// 			_this.c_height = img_bl * imgHeight
				// 			_this.init_canvas()
				// 		}
				// 	})
				// else {
					let _this = this
					uni.createSelectorQuery().select('#image').fields({size:true}).exec(function(res){
						const image = res[0]
						const h_w = image.height/image.width
						_this.c_height = 750 * h_w
						_this.init_canvas()
					})
				// }
			},
			init_canvas(){
				this.ctx = uni.createCanvasContext("mycanvas", this);
				this.ctx.lineWidth = 8;
				this.ctx.lineCap = "round"
				this.ctx.lineJoin = "round"
			},
			touchstart: function(e) {
				let startX = e.changedTouches[0].x;
				let startY = e.changedTouches[0].y;
				let startPoint = {
					X: startX,
					Y: startY
				};

				this.points.push(startPoint);

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
				let _this = this
				this.ctx.draw(true, () => {
					uni.canvasToTempFilePath({
						canvasId: 'mycanvas',
						fileType: "jpg",
						success: function(res) {
							let path = res.tempFilePath;
							pathToBase64(path).then(base64 => {
								uni.setStorageSync('mask', base64)
								_this.$refs.toast.show({
									message:'绘制成功',
									type:"success",
									position:'top',
									complete:function(){
										uni.navigateBack()
									}
								})
							}).catch(e => {
								console.log(e)
							})
						}
					})
				})
			}
		}
	}
</script>

<style lang='scss' scoped>
	.row {
		width: 750rpx;
		height: 100vh;
		overflow-y: hidden;
		background-color:white;
		.info{
			color:  #FF5A5F;
			font-size: 30rpx;
			font-style: italic;
		}
		.button_area {
			margin-top: 50rpx;
			width: 250rpx;
			height: 100rpx;
			margin-left: 250rpx;
			display: flex;
			.delete_button{
				width: 100rpx;
				margin-right: 50rpx;
			}
		}
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