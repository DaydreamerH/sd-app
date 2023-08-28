<template>
	<view class='row'>
		<view class='ImageBox'>
			<uv-image :src="info.source" width="750rpx" height="750rpx" mode="aspectFit"></uv-image>
		</view>
		<text class='Title'>
			{{info.title}}
		</text>
		<view class='WriterInfo'>
			<uv-avatar :src='info.painter_avatar' size='50' class='painter_avatar'></uv-avatar>
			<view class='PainterInfo'>
				<view class='painter_name'>{{info.painter_uname}}</view>
				<view class='painter_sign'>{{info.painter_sign}}</view>
			</view>
		</view>
		<view class='Main'>
			<view v-if='info.prompt!=""'>
				<text class='PartText'>正面词</text>
				<view class='Words'>{{info.prompt}}</view>
			</view>
			<view v-if='info.n_prompt!=""'>
				<text class='PartText'>负面词</text>
				<view class='Words'>{{info.n_prompt}}</view>
			</view>
			<view class='PartText'>所用模型</view>
			<view class='tag'>{{info.tag}}</view>
			<view class='time'>
				{{info.img_time}}
			</view>
			<view class='time'>
				{{info.like_num}}人赞了
			</view>
			<view style='display: flex;'>
				<uv-button icon='star' shape='circle' class='StarButton' type='primary' plain @click="like"></uv-button>
				<uv-button icon='download' shape='circle' class='DownButton' type='primary' plain
					@click="download"></uv-button>
			</view>
		</view>
		<uv-gap height="10rpx" bgColor="#f3f4f6"></uv-gap>
		<view>

		</view>
		<uv-button class='CommentButton' icon="edit-pen" shape='circle' @click="OpenComment"></uv-button>
		<uv-popup ref='popup' round="20rpx">
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
		onPullDownRefresh(){
			this.page = 1
			this.commentSelect()
			uni.stopPullDownRefresh()
		}
	}
</script>

<style lang='scss' scoped>
	.row {
		width: 750rpx;
		height: 100vh;

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

			.PainterInfo {
				display: block;
				width: 400rpx;
				height: auto;

				.painter_name {
					font-weight: 350;
					margin-left: 10rpx;
					margin-top: 15rpx;
					font-size: 40rpx;
				}

				.painter_sign {
					margin-left: 10rpx;
					font-size: 30rpx;
					margin-top: 20rpx;
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

			.PartText {
				font-size: 40rpx;
				margin-left: 25rpx;
			}

			.Words {
				margin-top: 20rpx;
				width: 700rpx;
				height: auto;
				background-color: gray;
				margin-left: 25rpx;
				padding-left: 10rpx;
				padding-right: 10rpx;
				padding-top: 20rpx;
				padding-bottom: 20rpx;
				margin-bottom: 20rpx;
				border-radius: 20rpx;
			}

			.tag {
				margin-left: 25rpx;
				margin-bottom: 20rpx;
				margin-top: 20rpx;
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