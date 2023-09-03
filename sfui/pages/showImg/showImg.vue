<template>
	<view class='row'>
		<view class='ImageBox'>
			<uv-image :src="info.source" width="750rpx" height="750rpx" mode="aspectFit"></uv-image>
		</view>
		<text class='Title'>
			{{info.title}}
		</text>
		<view class='WriterInfo'>
			<uv-avatar :src='info.painter_avatar' size='40' class='painter_avatar'></uv-avatar>
			<view class='PainterInfo'>
				<view class='painter_name'>{{info.painter_uname}}</view>
				<view class='painter_sign'>{{info.painter_sign}}</view>
			</view>
			<view class='up_info' @click="toOtherSpace" v-if='u_info.uid!=info.painter_uid'>
				进入ta的空间
			</view>
		</view>
		<view class='Main'>
			<view v-if='info.prompt!=""'>
				<view class='Words'>
					<view class='PartText'>正面词</view>
					<view class='Text'>{{info.prompt}}</view>
				</view>
			</view>
			<view v-if='info.n_prompt!=""'>
				<view class='Words'>
					<view class='PartText'>负面词</view>
					<view class='Text'>{{info.n_prompt}}</view>
				</view>
			</view>
			<view class='Words'>
				<view class='PartText'>所用模型:&ensp;{{info.tag}}</view>
			</view>
			<view class='time'>
				{{info.img_time}}
			</view>
			<view class='time'>
				{{info.like_num}}人赞了
			</view>
			<view style='display: flex;'>
				<uv-button icon='star' shape='circle' class='StarButton' @click="like" color="#008080"
					iconColor="white"></uv-button>
				<uv-button icon='download' shape='circle' class='DownButton' type='primary' @click="download"
					color="#008080" iconColor="white"></uv-button>
			</view>
		</view>
		<uv-gap height="10rpx" bgColor="#f3f4f6"></uv-gap>
		<view>

		</view>
		<uv-button class='PaintButton' icon="photo" @click="toPaint" color="#D2E8E8"
			iconColor="#008080"></uv-button>
		<uv-button class='CommentButton' icon="edit-pen" @click="OpenComment" color="#D2E8E8"
			iconColor="#008080"></uv-button>
		<uv-popup ref='popup' round="10rpx">
			<text class='GiveTitle'>评论</text>
			<view>
				<uv-input v-model='comment_text' class='TitleInput' placeholder="字数不超过20字" maxlength="20"></uv-input>
			</view>
			<uv-button @click="PostComment" class='UpButton'>发表</uv-button>
		</uv-popup>
		<view>
			<view class='comTitle'>最新评论</view>
			<view v-for='(comment,index) in info.com_list' :key='index'>
				<Comment :comment="comment" v-if='show_time'></Comment>
			</view>
		</view>
		<uv-load-more :status="loadAble"></uv-load-more>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				info: "",
				params: {
					width: "750rpx",
					height: "800rpx",
					blur: "xs",
					image: ''
				},
				u_info: {
					uid: '',
					secret: ''
				},
				iid: '',
				comment_text: '',
				page: 1,
				per_page: 4,
				show_time: false,
				loadAble: 'loadmore'
			}
		},
		methods: {
			commentSelect() {
				let _this = this
				const form = {
					iid: _this.iid,
					page: _this.page,
					per_page: _this.per_page,
				}
				if (this.page == 1) this.show_time = false
				else form['cid'] = this.info.com_list[0].cid
				uni.request({
					url: "http://localhost:3689/comment/select",
					method: 'POST',
					data: form
				}).then(function(resp) {
					if (_this.page == 1) {
						_this.info.com_list = resp.data.com_list
						_this.show_time = true
					} else _this.info.com_list = _this.info.com_list.concat(resp.data.com_list)
					_this.info.total_compage = resp.data.total_pages
				})
			},
			like() {
				let _this = this
				const form = {
					uid: _this.u_info.uid,
					secret: _this.u_info.secret,
					iid: this.iid
				}
				if (!this.info.like_state) {
					uni.request({
						url: "http://localhost:3689/like/insert",
						data: form,
						method: "POST"
					}).then(function(resp) {
						if (resp.data == 'success') {
							_this.info.like_state = 1
							_this.info.like_num += 1
						}
					})
				} else {
					uni.request({
						url: "http://localhost:3689/like/delete",
						data: form,
						method: "POST"
					}).then(function(resp) {
						if (resp.data == 'success') {
							_this.info.like_state = 0
							_this.info.like_num -= 1
						}
					})
				}
			},
			download() {
				let _this = this
				uni.downloadFile({
					url: _this.info.source, // 图像的网络地址
					success: function(res) {
						if (res.statusCode === 200) {
							uni.saveImageToPhotosAlbum({
								filePath: res.tempFilePath,
								success: function() {
									uni.showToast({
										title: '保存成功',
										icon: 'success'
									});
								},
								fail: function(error) {
									uni.showToast({
										title: '保存失败',
										icon: 'none'
									});
									console.log(error);
								}
							});
						} else {
							console.log('下载失败');
						}
					},
					fail: function(error) {
						console.log('下载失败');
						console.log(error);
					}
				});
			},
			PostComment() {
				if(this.comment_text==''){
					uni.showToast({
						title:'评论不得为空',
						icon:'error'
					})
					return false
				}
				else if(this.comment_text.length>20){
					uni.showToast({
						title:'评论在20字以内',
						icon:'error'
					})
					return false
				}
				const form = {
					iid: this.iid,
					uid: this.u_info.uid,
					secret: this.u_info.secret,
					text: this.comment_text
				}
				let _this = this
				uni.request({
					url: 'http://localhost:3689/comment/insert',
					method: 'POST',
					data: form
				}).then(function(resp) {
					_this.info.com_list.unshift(resp.data)
					uni.showToast({
						title: '发表成功'
					})
					_this.$refs.popup.close()
				})
			},
			OpenComment() {
				this.$refs.popup.open()
			},
			toPaint(){
				uni.reLaunch({
					url:'/pages/Paint/Paint?prompt='+this.info.prompt+'&n_prompt='+this.info.n_prompt
				})
			},
			toOtherSpace(){
				uni.navigateTo({
					url:'/pages/OtherSpace/OtherSpace?uid='+this.info.painter_uid
				})
			}
		},
		onLoad(option) {
			let _this = this
			const iid = option.iid
			this.iid = iid
			uni.getStorage({
				key: "u_info",
				success(res) {
					_this.u_info.secret = res.data.secret
					_this.u_info.uid = res.data.uid
					const form = {
						uid: _this.u_info.uid,
						iid: iid,
						per_page: _this.per_page
					}
					uni.request({
						url: "http://localhost:3689/img/show",
						method: "POST",
						data: form
					}).then(function(resp) {
						if (resp.data != "error") {
							_this.info = resp.data
							_this.params.image = _this.info.source
							if (resp.data.com_list != []) _this.show_time = true
						} else {
							uni.showToast({
								icon: None,
								title: "查询失败"
							})
						}
					})
				}
			})
		},
		onReachBottom() {
			this.page += 1

			if (this.page > this.info.total_compage) {
				this.loadAble = 'nomore'
				this.page -= 1
			} else {
				this.loadAble = 'loading'
				this.commentSelect()
				this.loadAble = 'loadmore'
			}
		},
		onPullDownRefresh() {
			this.page = 1
			this.commentSelect()
			uni.stopPullDownRefresh()
		}
	}
</script>

<style lang='scss' scoped>
	.row {
		width: 750rpx;
		min-height: 100vh;
		height: auto;
		overflow-x: hidden;

		.ImageBox {
			width: 750rpx;
			height: 750rpx;
			background-color: black;
			margin-bottom: 20rpx;
		}

		.Title {
			font-size: 50rpx;
			margin-left: 20rpx;
			font-weight: 350;
		}

		.WriterInfo {
			width: 750rpx;
			height: 130rpx;
			display: flex;
			margin-top: 20rpx;
			margin-left: 10rpx;
			.up_info{
				height: 30rpx;
				text-align: center;
				margin-top:25rpx;
				margin-left: 140rpx;
				font-size: 30rpx;
				background-color: #2A9D8F;
				color: white;
				border: solid 10rpx #2A9D8F;
				border-radius: 20rpx;
			}
			.PainterInfo {
				display: block;
				width: 300rpx;
				height: auto;

				.painter_name {
					font-weight: 350;
					margin-left: 10rpx;
					margin-top: 15rpx;
					font-size: 30rpx;
				}

				.painter_sign {
					margin-left: 10rpx;
					font-size: 25rpx;
					margin-top: 20rpx;
					color: darkgray;
				}
			}

			.painter_avatar {
				margin-top: 10rpx;
			}
		}

		.Main {
			margin-top: 20rpx;
			width: 750rpx;
			height: auto;
			margin-bottom: 20rpx;

			.Words {
				box-shadow: 0 5rpx 5rpx rgba(0, 0, 0, 0.1);
				.PartText {
					font-size: 40rpx;
					margin-bottom: 10rpx;
				}
				.Text{
					background-color: #8AC0C0;
					margin: 10rpx;
					padding: 20rpx;
					border-radius: 10rpx;
				}
				margin-top: 20rpx;
				width: 700rpx;
				height: auto;
				margin-left: 20rpx;
				padding-left: 10rpx;
				padding-right: 10rpx;
				padding-top: 20rpx;
				padding-bottom: 20rpx;
				margin-bottom: 20rpx;
				background-color: #008080;
				color:white;
			}

			.tag {
				margin-left: 25rpx;
				margin-bottom: 20rpx;
				margin-top: 20rpx;
				color: #008080;
			}

			.time {
				text-align: center;
				color: darkgray;
				margin-top: 10rpx;
				font-size: 25rpx;
			}

			.StarButton {
				width: 100rpx;
				margin-left: 250rpx;
				margin-top: 20rpx;
				margin-bottom: 10rpx;
			}

			.DownButton {
				width: 100rpx;
				margin-left: 30rpx;
				margin-top: 20rpx;
				margin-bottom: 10rpx;
			}
		}

		.CommentButton {
			bottom: 30rpx;
			right: 30rpx;
			position: fixed;
			width: 100rpx;
			box-shadow: 0 5rpx 5rpx rgba(0, 0, 0, 0.1);
			border-radius: 30rpx;
		}
		.PaintButton{
			bottom: 140rpx;
			right: 30rpx;
			position: fixed;
			width: 100rpx;
			box-shadow: 0 5rpx 5rpx rgba(0, 0, 0, 0.1);
			border-radius: 30rpx;
		}
		
		.GiveTitle {
			margin: 20rpx;
			font-size: larger;
			font-weight: bold;
		}

		.TitleInput {
			width: 600rpx;
			margin: 40rpx;
		}

		.UpButton {
			width: 200rpx;
			margin-left: 240rpx;
			margin-bottom: 20rpx;
		}

		.comTitle {
			margin-top: 8rpx;
			margin-left: 10rpx;
			margin-bottom: 10rpx;
		}
	}
</style>