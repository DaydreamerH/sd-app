<template>
	<view class="row">
		<uv-search v-model='con' @custom="search" class='Search'></uv-search>
		<view v-for='(imgs,index) in pairedPrevImgs' :key='index' class="ImgsBox">
			<view v-for='(img,index) in imgs' :key='img.iid'>
				<view v-if='show_time&&index==0' @click="toShow(img.iid)">
					<ImgCard v-if='show_time&&index==0' :img_url='img.source' :title='img.title'></ImgCard>
				</view>
				<view v-if='show_time&&index==1' @click="toShow(img.iid)">
					<ImgCardRight v-if='show_time&&index==1' :img_url='img.source' :title='img.title'></ImgCardRight>
				</view>
			</view>
		</view>
		<uv-load-more :status="loadAble"></uv-load-more>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				result: [],
				page: 1,
				per_page: 6,
				total_pages: '',
				show_time: false,
				con:'',
				loadAble:'loadmore'
			};
		},
		methods: {
			getImg(){
				let form={}
				if(this.page == 1){
					form={
						page:this.page,
						per_page:this.per_page,
						con:this.con
					}
					this.show_time = false
				}
				else {
					form={
						page:this.page,
						per_page:this.per_page,
						con:this.con,
						iid:this.result[0].iid
					}
				}
				let _this = this
				uni.request({
					data:form,
					method:"POST",
					url:'http://localhost:3689/img/select_con'
				}).then(function(resp){
					if(_this.page == 1){
						_this.result = resp.data.img_list
						_this.show_time = true
					}
					else _this.result = _this.result.concat(resp.data.img_list)
					_this.total_pages = resp.data.total_pages
				})
			},
			toShow(iid) {
				uni.navigateTo({
					url: '/pages/showImg/showImg?iid=' + iid
				})
			},
			search(){
				this.page = 1
				this.getImg()
			}
		},
		onLoad(option) {
			this.con = option.con
			const form = {
				page: this.page,
				per_page: this.per_page,
				con: this.con
			}
			let _this = this
			uni.request({
				url: 'http://localhost:3689/img/select_con',
				method: 'POST',
				data: form
			}).then(function(resp) {
				_this.result = resp.data.img_list
				_this.total_pages = resp.data.total_pages
				_this.show_time = true
			})
		},
		computed: {
			pairedPrevImgs() {
				const pairedPrevImgs = []
				for (let i = 0; i < this.result.length; i += 2) {
					const pair = this.result.slice(i, i + 2)
					pairedPrevImgs.push(pair)
				}
				return pairedPrevImgs
			}
		},
		onReachBottom(){
			this.page += 1
			if(this.page>this.total_pages)
			{
				this.page-=1
				this.loadAble='nomore'
			}
			else {
				this.loadAble='loading'
				this.getImg()
				this.loadAble='loadmore'
			}
		},
		onPullDownRefresh(){
			this.page = 1
			this.getImg()
			uni.stopPullDownRefresh()
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;

		.ImgsBox {
			display: flex;
			margin-top: 10rpx;
		}
		.Search{
			position: relative;
			top:10rpx;
		}
	}
</style>